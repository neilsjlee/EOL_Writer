import can
import can.interfaces.vector
from threading import Thread
import threading
import time
import queue

class CANSignal:
    def __init__(self, id, packet, extended):
        self.id = id
        self.packet = packet
        self.extended = extended

class CANConnection:
    def __init__(self, id, handler_funcs, channel = 0, bitrate=None, app_name="", fd=False):
        self.id = id
        self.can_bitrate = 500000
        self.can_bus = None
        self.can_app_name = "CANalyzer"
        self.can_channel = channel
        self.can_is_fd = fd
        self.queue = queue.Queue()
        self.is_stop = True

        if bitrate is not None:
            self.can_bitrate = bitrate

        if len(app_name) > 0:
            self.can_app_name = app_name

        self.callback_transmitted = handler_funcs[0]
        self.callback_received = handler_funcs[1]
        self.lock = threading.Condition()
        self.is_ready = self.create_connection()

    def send_message(self, index, parameters, id, packet, extended=False):
        self.lock.acquire()
        while True:
            if self.queue.empty():
                break
            self.lock.wait()
            break
        signal = {'index': index, 'id' : id, 'packet': packet, 'extended' : extended, 'parameters': parameters}
        self.queue.put(signal)
        self.lock.notify()
        self.lock.release()

    def process_message(self, lock):
        while True:
            if self.is_stop:
                break
            acquired = lock.acquire()
            while self.queue.empty():
                lock.wait()

            signal = self.queue.get()
            lock.release()
            result = self.transmit_message(signal['packet'], signal['id'], signal['extended'])
            self.callback_transmitted(signal['index'],signal['parameters'], result)
        print("process_message quit")

    def receive_message(self):
        while True:
            if self.is_stop:
                break
            msg = self.can_bus._recv_internal(20)
            if msg[0] is not None:
                var = msg[0]
                self.callback_received(self.id, var)
        print("receive_message quit")

    def create_connection(self):
        try:
            self.can_bus = can.ThreadSafeBus(bustype="vector", app_name=self.can_app_name, channel=self.can_channel, bitrate=self.can_bitrate)
            self.func_transmit = Thread(target=self.process_message, args=(self.lock,))
            self.func_transmit.daemon = True
            self.func_receive = Thread(target=self.receive_message)
            self.func_receive.daemon = True
            return True
        except Exception as e:
            print("Error Occured", e)
            return False

    def start(self):
        if self.is_stop:
            self.is_stop = False
            self.func_transmit.start()
            self.func_receive.start()

    def stop(self):
        self.lock.acquire()
        self.is_stop = True
        self.lock.notify()
        self.lock.release()

    def transmit_message(self, packet, id, extended=False):
        if self.can_bus is None:
            return False

        if packet == None:
            return False

        if len(packet) == 0:
            return False

        packet_list = []
        message_count = 1

        if len(packet) > 8:
            message_count = ((len(packet) - (len(packet) % 8)) / 8) + 1

        for i in range(0, message_count):
            packet_list.append(packet[(i*8):(8*(i+1))])

        for payload in packet_list:
            msg = can.Message(arbitration_id=id, data=payload, is_extended_id=extended)

            try:
                if msg is not None:
                    ret = self.can_bus.send(msg)
                    print("SENT Message : ", msg)
                else:
                    print("Message is not valid")
                    return False
            except can.CanError:
                print("Error occured while sending message")
                return False
        return True

    def set_filters(self, filters):
        if self.can_bus is not None:
            self.can_bus.set_filters(filters)
