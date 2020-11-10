from can_connector import CANConnection
from cluster_functions import *
import threading
import time

expected_message_list = []
is_started = False

def can_message_handler(connector, msg):
    id = msg.arbitration_id
    if id != DIAG_RES_ID:
        return

    print("RECV Message : ",msg)
    byte1 = msg.data[1]
    byte2 = msg.data[2]
    byte3 = msg.data[3]

    if byte1 == 0x50:
        if byte2 == 0x01:
            print("DIAG DEFAULT SESSION OK")
        if byte2 == 0x03:
            print("DIAG EXTENDED SESSION OK")
        if byte2 == 0x60:
            print("EOL SESSION OK")
        return
    if byte1 == 0x67:
        if byte2 == 0x01:
            print("KEY REQUEST NEEDED")
            request_key(connector, msg.data)
            print("SENT KEY")
        if byte2 == 0x02:
            print("EOL SECURITY UNLOCK SUCCESS")
            request_eol_write(connection, 0x5c, 0x4d)
        if byte2 == 0x61:
            request_key_visteon(connector, msg.data)
        if byte2 == 0x62:
            print("SECURITY UNLOCK SUCCESS")
        return

    if byte1 == 0x6E and byte2 == 0x00 and byte3 == 0x60:
        print("EOL CODE SUCCEFULLY WRITTEN")
        request_eol_read(connector)
        return
    if byte1 == 0x62 and byte2 == 0x00 and byte3 == 0x60:
        print("EOL CODE READED : ", hex(msg.data[4])," " ,hex(msg.data[5]))
        return

def can_recv(connector):
    global is_started
    global expected_message_list
    while True:
        if not is_started:
            ret_msg = request_extended_session(connection)
            if ret_msg is not None:
                print("EXTEND")
                expected_message_list.append(ret_msg)
            time.sleep(0.1)
            ret_msg = request_general_seed(connection)
            if ret_msg is not None:
                print("SEED")
                expected_message_list.append(ret_msg)
            time.sleep(0.1)
            #ret_msg = request_eol_write(connection, 0x5c, 0x4d)
            #if ret_msg is not None:
            #    print("EOL")
            #    expected_message_list.append(ret_msg)
            is_started = True
        msg = connector.recv_message()
        can_message_handler(connector, msg)


if __name__ == "__main__":
    eol_pre_packet = [0x5, 0x2E, 0x0, 0x60, 0x00, 0x00, 0x0, 0x0]

    connection = CANConnection()
    #set_response_filter(connection)
    recv = threading.Thread(target=can_recv, args=(connection,))
    recv.start()
