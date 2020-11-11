from os import path
from can_connector import CANConnection
import sys
import json
import importlib
import importlib.util
import threading
import time
import ctypes

REQUEST_FUNCTION    = 0
TRANSMIT_CALLBACK   = 1
RECEIVED_CALLBACK   = 2

class HKMCSignalHandler:
    def __init__(self, spec_filename, ui_param, log_function):
        if not path.exists(spec_filename):
            return
        if not path.isfile(spec_filename):
            return

        with open(spec_filename,"r") as self.scheme_file:
            self.logger = log_function
            self.scheme = json.load(self.scheme_file)
            self.connectors = []
            self.last_requested_signal = ""
            module_name = str(self.scheme['default_module'])
            spec = importlib.util.spec_from_file_location(module_name,""+module_name+".py")
            self.plugin = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(self.plugin)
            self.message_handler = getattr(self.plugin, "message_handler")
            setattr(self.plugin, 'g_ui_param', ui_param)
            setattr(self.plugin, 'g_signal_handler', self)
            setattr(self.plugin, 'g_logger_func', log_function)
            setattr(self.plugin, 'g_last_multi_frame_signal_cb', None)
            self.create_connectors()
            self.loaded_ask_dll = ""

    def start(self):
        for c in self.connectors:
            c.start()

    def stop(self):
        for c in self.connectors:
            c.stop()

    def get_signal_index(self, signal_name):
        index = 0
        for e in self.scheme['can_signals']:
            if e['name'] == signal_name:
                return index
            index = index + 1
        return -1

    def get_signal(self, signal_index):
        return self.scheme['can_signals'][index]

    def get_payload(self, index):
        payload_str = self.scheme['can_signals'][index]['payload']
        payload_num = []
        for e in payload_str:
            num = int(e, 16)
            payload_num.append(num)
        return payload_num

    def create_connectors(self):
        handler_funcs = [self.on_transmitted, self.on_received]
        index = 0
        for e in self.scheme['can_devices']:
            if e['enabled']:
                connector = CANConnection(index, handler_funcs, e['channel'], e['bitrate'], e['app_name'],e['is_fd'])
                if connector.is_ready:
                    self.connectors.append(connector)
                    index = index + 1

    def get_func(self, signal_index, function_type):
        if function_type == REQUEST_FUNCTION:
            name = self.scheme['can_signals'][signal_index]['request_function']
        if function_type == RECEIVED_CALLBACK:
            name = self.scheme['can_signals'][signal_index]['callback_recevied']
        if function_type == TRANSMIT_CALLBACK:
            name = self.scheme['can_signals'][signal_index]['callback_transmitted']
        if name == None:
            return None
        try:
            func = getattr(self.plugin, name)
        except Exception as e:
            func = None
        target = self.scheme['can_signals'][signal_index]['target']
        channel = -1
        id = -1
        for e in self.scheme['can_targets']:
            if e['name'] == target:
                channel = e['channel']
                id = int(e['address'] ,16)
                break
        return func, channel, id

    def do_request(self, signal_name, parameters=None, remain_history=True):
        signal_index = self.get_signal_index(signal_name)
        if signal_index < 0:
            print("Invalid signal index")
            return False
        func, channel, id = self.get_func(signal_index, REQUEST_FUNCTION)
        if func == None:
            return False
        try:
            packet, extended = func(self.scheme['can_signals'][signal_index], parameters)
            self.connectors[channel].send_message(signal_index, parameters, id, packet, extended)
        except Exception as e:
            print(str(e), parameters, signal_name)
            if self.logger is not None:
                self.logger("request function failure : ", signal_name)
            return False
        if remain_history:
            self.last_requested_signal = signal_name
        return True

    def on_transmitted(self, signal_index, parameters, transmitted):
        func, channel, id = self.get_func(signal_index,TRANSMIT_CALLBACK)
        if func == None:
            return False
        try:
            func(self.scheme['can_signals'][signal_index], parameters, transmitted)
        except:
            if self.logger is not None:
                self.logger("on_transmitted function failure : ", signal_index)
        return True

    def on_received(self, id, packet):
        # Fetch signals
        return self.message_handler(self.connectors[id], self.last_requested_signal, packet)

    def load_ask_dll(self, loaded):
        self.loaded_ask_dll = loaded

    def calculate_ask_key(self, received_ask_seed):
        py_arr = [0, 0, 0, 0, 0, 0, 0, 0]
        i = 0
        while (i < 8):
            py_arr[i] = int(received_ask_seed[i], 16)
            i = i + 1
        c_arr = (ctypes.c_byte * len(py_arr))(*py_arr)

        py_arr2 = [0, 0, 0, 0, 0, 0, 0, 0]
        result_c = (ctypes.c_byte * len(py_arr2))(*py_arr2)

        self.loaded_ask_dll.ASK_KeyGenerate(c_arr, result_c)

        result = []
        i = 0
        while (i < 8):
            temp = result_c[i]
            if temp < 0:
                temp = temp + 256
            print(temp)
            result.append(temp)
            i = i + 1

        return result