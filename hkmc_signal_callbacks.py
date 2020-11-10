import os
from can_connector import CANConnection

g_ui_param = None
g_signal_handler = None
g_logger_func = None
g_last_multi_frame_signal_cb = 0
l_part_number = [0,0,0,0,0,0,0,0,0,0]

def convert_signal(signal):
    converted_signal = list()
    for e in signal:
        converted_signal.append(int(e,16) & 0xFF)
    return converted_signal
def request_tester_present(base_signal, msg):
    return convert_signal(base_signal['payload']), False

def tester_present_transmitted_cb(signal_index, parameters, transmitted):
    print("TRANSMITTED", transmitted, parameters)

def request_internal_sw_version(base_signal, msg):
    return convert_signal(base_signal['payload']), False

def request_part_number(base_signal, msg):
    return convert_signal(base_signal['payload']), False

def request_part_number_transmitted_cb(signal_index, parameters, transmitted):
    print("TRANSMITTED", transmitted, parameters)

def request_internal_sw_version_transmitted_cb(signal_index, parameters, transmitted):
    print("TRANSMITTED", transmitted, parameters)

def request_manuf_date(base_signal, msg):
    return convert_signal(base_signal['payload']), False

def request_manuf_date_transmitted_cb(signal_index, parameters, transmitted):
    print("TRANSMITTED", transmitted, parameters)

def request_sw_version(base_signal, msg):
    return convert_signal(base_signal['payload']), False

def request_sw_version_transmitted_cb(signal_index, parameters, transmitted):
    print("TRANSMITTED", transmitted, parameters)

def request_hw_version(base_signal, msg):
    return convert_signal(base_signal['payload']), False

def request_hw_version_transmitted_cb(signal_index, parameters, transmitted):
    print("TRANSMITTED", transmitted, parameters)

def request_mmcan_version(base_signal, msg):
    return convert_signal(base_signal['payload']), False

def request_mmcan_version_transmitted_cb(signal_index, parameters, transmitted):
    print("TRANSMITTED", transmitted, parameters)

def request_default_session(base_signal, msg):
    return convert_signal(base_signal['payload']), False

def default_session_transmitted_cb(signal_index, parameters, transmitted):
    print("TRANSMITTED", transmitted, parameters)

def request_extended_diag_session(base_signal, msg):
    return convert_signal(base_signal['payload']), False

def extended_diag_session_transmitted_cb(signal_index, parameters, transmitted):
    print("TRANSMITTED", transmitted, parameters)

def request_eol_session(base_signal, msg):
    return convert_signal(base_signal['payload']), False
def eol_session_transmitted_cb(signal_index, parameters, transmitted):
    print("TRANSMITTED", transmitted, parameters)

def request_programming_session(base_signal, msg):
    return convert_signal(base_signal['payload']), False

def programming_session_transmitted_cb(signal_index, parameters, transmitted):
    print("TRANSMITTED", transmitted, parameters)

def request_extended_diag_mode(base_signal, msg):
    print("DIAG MODE")
    return convert_signal(base_signal['payload']), False

def extended_diag_mode_transmitted_cb(signal_index, parameters, transmitted):
    print("TRANSMITTED", transmitted, parameters)

def request_general_seed(base_signal, parameter):
    return convert_signal(base_signal['payload']), False

def general_seed_transmitted_cb(signal_index, parameters, transmitted):
    print("TRANSMITTED", transmitted, parameters)

def request_visteon_seed(base_signal, parameter):
    return convert_signal(base_signal['payload']), False

def visteon_seed_transmitted_cb(signal_index, parameters, transmitted):
    print("TRANSMITTED", transmitted, parameters)



def request_key(base_signal, parameter):
    key_packet = bytearray(4)
    key_packet[0] = parameter[3] ^ 0xFF
    key_packet[1] = parameter[4] ^ 0xFF
    key_packet[2] = parameter[5] ^ 0xFF
    key_packet[3] = parameter[6] ^ 0xFF
    key_packet[3] = key_packet[3] + 0x0D
    signal = convert_signal(base_signal['payload'])
    for i in range(3,7):
        print(i, (i-3))
        signal[i] = key_packet[i-3]
    return signal, False

def key_transmitted_cb(signal_index, parameters, transmitted):
    print("TRANSMITTED", transmitted, parameters)

def request_visteon_key(base_signal, parameter):
    key_packet = bytearray(4)
    key_packet[0] = parameter[3] ^ 0xFF
    key_packet[1] = parameter[4] ^ 0xFF
    key_packet[2] = parameter[5] ^ 0xFF
    key_packet[3] = parameter[6] ^ 0xFF
    key_packet[3] = (key_packet[3] + 0x56) & 0xFF
    signal = convert_signal(base_signal['payload'])
    for i in range(3,7):
        print(i, (i-3))
        signal[i] = key_packet[i-3]
    return signal, False

def visteon_key_transmitted_cb(signal_index, parameters, transmitted):
    print("TRANSMITTED", transmitted, parameters)

def request_config_read(base_signal, parameter):
    print("CONFIG_READ_")
    return convert_signal(base_signal['payload']), False

def config_read_transmitted_cb(signal_index, parameters, transmitted):
    print("TRANSMITTED", transmitted, parameters)

def request_sw_reset(base_signal, parameter):
    return convert_signal(base_signal['payload']), False

def request_sw_reset_transmitted_cb(signal_index, parameters, transmitted):
    print("TRANSMITTED", transmitted, parameters)

def request_odo_reset(base_signal, parameter):
    return convert_signal(base_signal['payload']), False

def request_odo_reset_transmitted_cb(signal_index, parameters, transmitted):
    print("TRANSMITTED", transmitted, parameters)

def request_chime_test(base_signal, parameter):
    signal = convert_signal(base_signal['payload'])
    if parameter != None:
        signal[5] = parameter[0]
    return signal, False

def chime_test_transmitted_cb(signal_index, parameters, transmitted):
    print("TRANSMITTED", transmitted, parameters)

def request_chime_release(base_signal, parameter):
    return convert_signal(base_signal['payload']), False

def chime_release_transmitted_cb(signal_index, parameters, transmitted):
    print("TRANSMITTED", transmitted, parameters)

def request_eol_write(base_signal, parameter):
    signal = convert_signal(base_signal['payload'])
    signal[4] = parameter[0]
    signal[5] = parameter[1]

    if g_ui_param['eol_length'].get() == 4:
        signal[0] = 0x07
        signal[6] = parameter[2]
        signal[7] = parameter[3]

    return signal, False

def request_eol_write_transmitted_cb(signal_index, parameters, transmitted):
    print("TRANSMITTED", transmitted, parameters)

def request_eol_read(base_signal, parameter):
    return convert_signal(base_signal['payload']), False

def request_supported_pid(base_signal, parameter):
    global g_last_multi_frame_signal_cb
    g_last_multi_frame_signal_cb = response_supported_pid_cb
    return convert_signal(base_signal['payload']), False

def request_io_record1(base_signal, parameter):
    global g_last_multi_frame_signal_cb
    if g_last_multi_frame_signal_cb != response_io_record1_cb and g_last_multi_frame_signal_cb != None:
        print("ANOTHER MULTI FRAME COMMUNICATION PROCESSED", g_last_multi_frame_signal_cb)
        return None, False
    g_last_multi_frame_signal_cb = response_io_record1_cb
    return convert_signal(base_signal['payload']), False

def io_record1_transmitted_cb(signal_index, parameters, transmitted):
    print("TRANSMITTED", transmitted, parameters)

def request_io_record2(base_signal, parameter):
    global g_last_multi_frame_signal_cb
    g_last_multi_frame_signal_cb = response_io_record2_cb
    return convert_signal(base_signal['payload']), False

def request_visteon_eol_read(base_signal, parameter):
    global g_last_multi_frame_signal_cb
    g_last_multi_frame_signal_cb = response_visteon_eol_read_cb
    return convert_signal(base_signal['payload']), False

def request_visteon_eol_write(base_signal, parameter):
    signal = convert_signal(base_signal['payload'])
    signal[5] = parameter[0]
    signal[6] = parameter[1]
    signal[7] = parameter[2]
    return signal, False

def request_visteon_eol_write_transmitted_cb(signal_index, parameters, transmitted):
    print("TRANSMITTED", transmitted, parameters)

def request_odo_write(base_signal, parameter):
    return convert_signal(base_signal['payload']), False

def odo_write_transmitted_cb(signal_index, parameters, transmitted):
    print("TRANSMITTED", transmitted, parameters)

def request_telltale_all_on(base_signal, parameter):
    return convert_signal(base_signal['payload']), False

def telltale_all_on_transmitted_cb(signal_index, parameters, transmitted):
    print("TRANSMITTED", transmitted, parameters)

def request_gauge_sweep(base_signal, parameter):
    return convert_signal(base_signal['payload']), False

def gauge_sweep_transmitted_cb(signal_index, parameters, transmitted):
    print("TRANSMITTED", transmitted, parameters)

def request_telltale_all_off(base_signal, parameter):
    return convert_signal(base_signal['payload']), False

def telltale_all_off_transmitted_cb(signal_index, parameters, transmitted):
    print("TRANSMITTED", transmitted, parameters)


def request_eol_write_transmitted_cb(signal_index, parameters, transmitted):
    print("TRANSMITTED", transmitted, parameters)

def request_pointer_replacement(base_signal, parameter):
    return convert_signal(base_signal['payload']), False

def pointer_replacement_transmitted_cb(signal_index, parameters, transmitted):
    print("TRANSMITTED", transmitted, parameters)

def request_multi_frame_write(base_signal, parameter):
    signal = convert_signal(base_signal['payload'])
    print(parameter)
    index = 1
    for e in parameter:
        signal[index] = e
        index += 1
    print(signal)
    return signal, False

def request_multi_frame_read(base_signal, paramater):
    return convert_signal(base_signal['payload']), False

def multi_frame_read_transmitted_cb(signal_index, parameters, transmitted):
    print("TRANSMITTED", transmitted, parameters)

def response_default_session_cb(connector, msg):
    print("DEFAULT SESSION OK")
    g_ui_param['session'] = msg.data[2]
    return True

def response_extended_session_cb(connector, msg):
    g_ui_param['session'] = msg.data[2]
    print("EXTENDED SESSION OK")
    return True

def response_extended_diag_session_cb(connector, msg):
    g_ui_param['session'] = msg.data[2]
    print("EXTENDED DIAG SESSION OK")
    return True

def response_programming_session_cb(connector, msg):
    g_ui_param['session'] = msg.data[2]
    print("EOL PROGRAMMING SESSION OK")
    return True

def response_eol_session_cb(connector, msg):
    g_ui_param['session'] = msg.data[2]
    print("EOL SESSION OK")
    return True

def response_sw_reset_cb(connector, msg):
    print("SOFTWARE RESET SUCCESSFULLY")
    return True

def response_key_cb(connector, msg):
    print("EOL SECURITY UNLOCK SUCCESS")
    return True

def response_general_seed_cb(connector, msg):
    print("SEED RECEIVED, REQUEST KEY_CUSTOMER", msg.data)
    g_signal_handler.do_request("REQUEST_KEY", msg.data)
    return True

def response_visteon_seed_cb(connector, msg):
    print("KEY_VISTEON", msg.data)
    g_signal_handler.do_request("REQUEST_VISTEON_KEY", msg.data)
    return True

def response_visteon_key_cb(connector, msg):
    print("VISTEON SECURITY UNLOCK SUCCESS")
    return True

def response_eol_write_cb(connector, msg):
    print("EOL CODE SUCCEFULLY WRITTEN")
    return True

def response_eol_read_cb(connector, msg):
    print("EOL CODE READED : ", hex(msg.data[4])," " ,hex(msg.data[5]))
    eol_byte_1 = g_ui_param['eol_byte_1']
    eol_byte_2 = g_ui_param['eol_byte_2']

    eol_byte_1.set(str(hex(msg.data[4])).replace("0x","").upper())
    eol_byte_2.set(str(hex(msg.data[5])).replace("0x","").upper())

    if msg.data[0] == 7:
        eol_byte_3 = g_ui_param['eol_byte_3']
        eol_byte_4 = g_ui_param['eol_byte_4']

        eol_byte_3.set(str(hex(msg.data[6])).replace("0x","").upper())
        eol_byte_4.set(str(hex(msg.data[7])).replace("0x","").upper())
        g_ui_param['eol_length'].set(4)
    else:
        g_ui_param['eol_length'].set(2)

    g_ui_param['eol_length_cb']()



    return True

def response_visteon_eol_read_cb(connector, msg):
    global g_last_multi_frame_signal_cb
    if msg.data[0] == 0x21:
        visteon_eol_byte_4 = g_ui_param['visteon_eol_byte_4']
        visteon_eol_byte_5 = g_ui_param['visteon_eol_byte_5']
        visteon_eol_byte_6 = g_ui_param['visteon_eol_byte_6']
        visteon_eol_byte_7 = g_ui_param['visteon_eol_byte_7']
        visteon_eol_byte_8 = g_ui_param['visteon_eol_byte_8']

        visteon_eol_byte_4.set(str(hex(msg.data[1])).replace("0x","").upper())
        visteon_eol_byte_5.set(str(hex(msg.data[2])).replace("0x","").upper())
        visteon_eol_byte_6.set(str(hex(msg.data[3])).replace("0x","").upper())
        visteon_eol_byte_7.set(str(hex(msg.data[4])).replace("0x","").upper())
        visteon_eol_byte_8.set(str(hex(msg.data[5])).replace("0x","").upper())
        g_last_multi_frame_signal_cb = None
    else:
        print("VISTEON EOL CODE READED : ", hex(msg.data[5])," " ,hex(msg.data[6]),hex(msg.data[7]))
        visteon_eol_byte_1 = g_ui_param['visteon_eol_byte_1']
        visteon_eol_byte_2 = g_ui_param['visteon_eol_byte_2']
        visteon_eol_byte_3 = g_ui_param['visteon_eol_byte_3']

        visteon_eol_byte_1.set(str(hex(msg.data[5])).replace("0x","").upper())
        visteon_eol_byte_2.set(str(hex(msg.data[6])).replace("0x","").upper())
        visteon_eol_byte_3.set(str(hex(msg.data[7])).replace("0x","").upper())
        g_last_multi_frame_signal_cb = response_visteon_eol_read_cb
        g_signal_handler.do_request("REQUEST_MULTI_FRAME_READ", None, False)
    return True

def response_visteon_eol_write(connector, msg):
    data = []
    data.append(int(g_ui_param['visteon_eol_byte_4'].get(), 16))
    data.append(int(g_ui_param['visteon_eol_byte_5'].get(), 16))
    data.append(int(g_ui_param['visteon_eol_byte_6'].get(), 16))
    data.append(int(g_ui_param['visteon_eol_byte_7'].get(), 16))
    data.append(int(g_ui_param['visteon_eol_byte_8'].get(), 16))
    print(data)
    g_signal_handler.do_request("REQUEST_MULTI_FRAME_WRITE", data)
    return True

def response_internal_sw_version_read_cb(connector, msg):
    major = msg.data[4]
    minor = msg.data[5]
    revision = msg.data[6]
    version = msg.data[4],".",msg.data[5],".",msg.data[6]
    version = major,".",minor,".",revision
    print("INTERNAL SW VERSION READED : ", version)
    g_ui_param['internal_sw_version'].set(version)
    return True

def change_part_digit(num):
    diff = int(str(hex(num - 0x30).split("x")[1]))
    if diff > 9:
        return hex(diff).split("x")[1].upper()
    else:
        return str(diff)

def response_part_number_read_cb(connector, msg):
    global g_last_multi_frame_signal_cb
    if msg.data[0] == 0x10 and msg.data[1] == 0x0d and msg.data[2] == 0x62:
        index = 0
        for e in msg.data[5:]:
            l_part_number[index] = change_part_digit(e)
            index += 1
        g_last_multi_frame_signal_cb = response_part_number_read_cb
        g_signal_handler.do_request("REQUEST_MULTI_FRAME_READ", None, False)
    else:
        index = 3
        for e in msg.data[1:]:
            l_part_number[index] = change_part_digit(e)
            index += 1
        part_left = "".join([str (e) for e in l_part_number[:5]])
        part_right ="".join([str (e) for e in l_part_number[5:]])
        g_ui_param['part_number'].set(part_left+"-"+part_right)
        g_last_multi_frame_signal_cb = None
        print(l_part_number)
    return True

def response_manuf_date_read_cb(connector, msg):
    date = []
    for e in msg.data[4:]:
        date.append(str(hex(e)).replace("0x",""))
    date_string =""
    date_string = date[0]+""+date[1]+"/"+date[2]+"/"+date[3]
    g_ui_param['manuf_date'].set(date_string)
    print("MANUFACTURING DATE READED", date_string)
    return True

def response_sw_version_read_cb(connector, msg):
    major = msg.data[4] - 0x30
    minor = msg.data[5] - 0x30
    revision = msg.data[6] - 0x30
    version = msg.data[4],".",msg.data[5],".",msg.data[6]
    version = major,".",minor,".",revision
    print("SW VERSION READED : ", version)
    g_ui_param['sw_version'].set(version)
    return True

def response_hw_version_read_cb(connector, msg):
    major = msg.data[4] - 0x30
    minor = msg.data[5] - 0x30
    revision = msg.data[6] - 0x30
    version = msg.data[4],".",msg.data[5],".",msg.data[6]
    version = major,".",minor,".",revision
    print("HW VERSION READED : ", version)
    g_ui_param['hw_version'].set(version)
    return True

def response_mmcan_version_read_cb(connector, msg):
    major = int(msg.data[4] - 0x30) % 10
    minor = int(msg.data[5] - 0x30)
    revision = int(msg.data[6] - 0x30)
    version = msg.data[4],".",msg.data[5],".",msg.data[6]
    version = major,".",minor,".",revision
    print("MMCAN DB VERSION READED : ", version)
    g_ui_param['mmcan_version'].set(version)
    return True

def response_supported_pid_cb(connector, msg):
    print(msg.data)
    g_signal_handler.do_request("REQUEST_MULTI_FRAME_READ", None, False)
    return True

def response_io_record1_cb(connector, msg):
    global g_last_multi_frame_signal_cb
    g_signal_handler.do_request("REQUEST_MULTI_FRAME_READ", None, False)
    if msg.data[0] == 0x21:
        g_last_multi_frame_signal_cb = None
        # Fuel
        if msg.data[2] == 0xFF:
            g_ui_param['fuel'].set("ERROR")
        else:
            g_ui_param['fuel'].set(str(float(msg.data[2]) * 0.5))
        
        # Battery
        g_ui_param['battery'].set(str(float(msg.data[3] * 0.08)))

        # odometer
        odo = 0
        odo |= msg.data[4] << 16
        odo |= msg.data[5] << 8
        odo |= msg.data[6]
        print(odo, msg.data[4], msg.data[5], msg.data[6])
        g_ui_param['odo_km'].set(str(odo))


    return True

def response_io_record2_cb(connector, msg):
    print(msg.data)
    g_signal_handler.do_request("REQUEST_MULTI_FRAME_READ", None, False)
    return True

def response_pointer_replacement_cb(connector, msg):
    print("POINTER_REPLACEMENT_REQUEST HAS BEEN ALLOWED")

def message_handler(connector, last_requested_signal, msg):
    id = msg.arbitration_id
    global g_last_multi_frame_signal_cb

    if id != 0x7ce:
        return

    print("RECV Message : ",msg)
    msg.data = list(msg.data)
    if len(msg.data) == 0:
        return

    #if last_requested_signal == "REQUEST_PART_NUMBER":
    #    return response_part_number_read_cb()

    byte0 = msg.data[0]
    byte1 = msg.data[1]
    byte2 = msg.data[2]
    byte3 = msg.data[3]
    byte4 = msg.data[4]
    byte5 = msg.data[5]

    if byte1 == 0x50:
        if byte2 == 0x01 or byte2 == 0x81:
            return response_default_session_cb(connector, msg)
        if byte2 == 0x03:
            return response_extended_session_cb(connector, msg)
        if byte2 == 0x60:
            return response_eol_session_cb(connector, msg)
        if byte2 == 0x85:
            return response_programming_session_cb(connector, msg)
        if byte2 == 0x90:
            return response_extended_diag_session_cb(connector, msg)

    if byte1 == 0x51:
        if byte2 == 0x03:
            return response_sw_reset_cb(connector, msg)

    if byte1 == 0x67:
        if byte2 == 0x01:
            return response_general_seed_cb(connector, msg)
        if byte2 == 0x02:
            return response_key_cb(connector, msg)
        if byte2 == 0x61:
            return response_visteon_seed_cb(connector, msg)
        if byte2 == 0x62:
            return response_visteon_key_cb(connector, msg)

    if byte1 == 0x6E:
        if byte2 == 0x00:
            if byte3 == 0x60:
                return response_eol_write_cb(connector, msg)
            if byte3 == 0x01:
                print("Variant configuration Successfull")

    if byte1 == 0x62:
        if byte2 == 0x00 and byte3 == 0x05:
            return response_internal_sw_version_read_cb(connector, msg)
        if byte2 == 0x00 and byte3 == 0x60:
            return response_eol_read_cb(connector, msg)

        if byte2 == 0xf1 and byte3 == 0x00:
            return response_mmcan_version_read_cb(connector, msg)
        if byte2 == 0xf1 and byte3 == 0x8b:
            return response_manuf_date_read_cb(connector, msg)
        if byte2 == 0xf1 and byte3 == 0x95:
            return response_sw_version_read_cb(connector, msg)
        if byte2 == 0xf1 and byte3 == 0x93:
            return response_hw_version_read_cb(connector, msg)
    if byte1 == 0x71:
        if byte3 == 0xFE and byte4 == 0x61 and byte5 == 0x03:
            return response_pointer_replacement_cb(connector, msg)

    if byte0 == 0x10:
        if byte1 == 0x0b:
            return response_visteon_eol_read_cb(connector, msg)
        if byte1 == 0x0d and byte3 == 0xf1 and byte4 == 0x87:
            return response_part_number_read_cb(connector, msg)
        if byte3 == 0xB0 and byte4 == 0x01:
            return response_supported_pid_cb(connector, msg)
        if byte3 == 0xB0 and byte4 == 0x02:
            return response_io_record1_cb(connector, msg)
        #if byte3 == 0xB0 and byte4 == 0x03:
        #    return response_io_record2_cb(connector, msg)

    if byte0 == 0x21 or byte0 == 0x22:
        print("MULTI FRAME RECEIVED", g_last_multi_frame_signal_cb)
        if g_last_multi_frame_signal_cb != None:
            g_last_multi_frame_signal_cb(connector, msg)
        print(last_requested_signal)
        #if last_requested_signal == "REQUEST_VISTEON_EOL_READ":
        #    return response_visteon_eol_read_cb(connector, msg)
        #if last_requested_signal == "REQUEST_PART_NUMBER":
        #    return response_part_number_read_cb(connector, msg)
        return False

    if byte0 == 0x30:
        if last_requested_signal == "REQUEST_VISTEON_EOL_WRITE":
            return response_visteon_eol_write(connector, msg)

    if byte1 == 0x7F:
        if byte2 == 0x2E and byte3 == 0x33:
            print("EOL CODE WRITE FAILURE")
    return False
