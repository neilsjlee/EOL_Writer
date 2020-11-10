from can import Message
from can_connector import CANConnection
import struct

cluster_function_array = []

DIAG_REQ_ID = 0x7c6
DIAG_RES_ID = 0x7ce
DIAG_FUN_ID = 0x7df

REQUEST_EXTENDED_DIAG_MODE = [0x02, 0x10, 0x90, 0x00, 0x00, 0x00, 0x00, 0x00]
REQUEST_EXTENDED_SESSION = [0x02, 0x10, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00]
REQUEST_GENERAL_SEED = [0x02, 0x27, 0x01, 0x00, 0x00, 0x00, 0x00]
REQUEST_ASK = [0x02, 0x27, 0x11, 0x00, 0x00, 0x00, 0x00]
REQUEST_SEED = [0x02, 0x27, 0x61, 0x00, 0x00, 0x00, 0x00, 0x00]
REQUEST_TEST_PRESENT = [0x02, 0x3E, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00]

REQUEST_EOL_WRITE = [0x05, 0x2E, 0x00, 0x60, 0x00, 0x00, 0x00, 0x00]
REQUEST_EOL_WRITE_VISTEON = [0x05, 0x2E, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00]
REQUEST_ODOMETER_WRITE = [0x05, 0x2E, 0x00, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0]
REQUEST_ODOMETER_RESET = [0x10, 0x2F, 0xFF, 0x00]

REQUEST_EOL_READ = [0x03, 0x22, 0x00, 0x60, 0x00, 0x00, 0x00, 0x00]
REQUEST_EOL_READ_VISTEON = [0x03, 0x22, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00]
REQUEST_SW_VERSION_READ = [0x03, 0x22, 0x00, 0x05, 0x00, 0x00, 0x00, 0x00]

REQUEST_KEY = [0x06, 0x27, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00]
REQUEST_KEY_VISTEON = [0x06, 0x27, 0x62, 0x00, 0x00, 0x00, 0x00, 0x00]

REQUEST_READ_ODOMETER_KM = [0x03, 0x22, 0xB0, 0x01]

# Control

REQUEST_SW_RESET = [0x02, 0x11, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00]
RESPONSE_SW_RESET = [0x03, 0x51, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00]

REQUEST_CHECK_DID_B000 = [0x03, 0x2F, 0xB0, 0x00, 0x02]
REQUEST_TELLTALE_ALL_ON = [0x05, 0x2F, 0xB0, 0x01, 0x03]
REQUEST_TELLTALE_ALL_OFF = [0x03, 0x2F, 0xB0, 0x02, 0x03]


RESPONSE_TEST_PRESENT = [0x03, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
RESPONSE_EXTENDED_SESSION = [0x03, 0x50, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
RESPONSE_GENERAL_SEED = [0x03, 0x67, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
RESPONSE_ASK = [0x03, 0x67, 0x11, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
RESPONSE_KEY = [0x03, 0x67, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
RESPONSE_KEY_VISTEON = [0x03, 0x67, 0x62, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
RESPONSE_EOL_WRITE = [0x03, 0x6E, 0x00, 0x60, 0x00, 0x00, 0x00, 0x00, 0x00]
RESPONSE_EOL_WRITE_VISTEON = [0x03, 0x6E, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00]
RESPONSE_EOL_READ = [0x03, 0x62, 0x00, 0x60, 0x00, 0x00, 0x00, 0x00, 0x00]
RESPONSE_EOL_READ_VISTEON = [0x03, 0x62, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00]



FILTER_DIAG_RESP = [{"can_id": DIAG_RES_ID, "can_mask": DIAG_RES_ID}]

def set_response_filter(connector):
    if connector is not None:
        connector.set_filters(FILTER_DIAG_RESP)

def request_test_present(connector):
    connector.send_message(REQUEST_TEST_PRESENT, DIAG_REQ_ID)
    return Message(arbitration_id=DIAG_RES_ID, data=RESPONSE_TEST_PRESENT)

def request_extended_diag_mode(connector):
    connector.send_message(REQUEST_EXTENDED_DIAG_MODE, DIAG_REQ_ID)
    return None

def request_write_odometer(connector, distance):
    odo_packet = REQUEST_ODOMETER_WRITE
    packed = struct.pack('<I', distance)
    odo_packet[9] = packed[3]
    odo_packet[10] = packed[2]
    odo_packet[11] = packed[1]
    odo_packet[12] = packed[0]
    connector.send_message(odo_packet, DIAG_REQ_ID, True)
    return Message(arbitration_id=DIAG_RES_ID, data=RESPONSE_SW_RESET)

def request_odometer_reset(connector):
    connector.send_message(REQUEST_ODOMETER_RESET, DIAG_REQ_ID)
    return None

def request_read_odometer_km(connector):
    connector.send_message(REQUEST_READ_ODOMETER_KM, DIAG_REQ_ID)
    return Message(arbitration_id=DIAG_RES_ID, data=RESPONSE_SW_RESET)

def request_sw_reset(connector):
    connector.send_message(REQUEST_SW_RESET, DIAG_REQ_ID)
    return Message(arbitration_id=DIAG_RES_ID, data=RESPONSE_SW_RESET)

def request_check_did_b000(connector):
    connector.send_message(REQUEST_CHECK_DID_B000, DIAG_REQ_ID)
    return None
    #return Message(arbitration_id=DIAG_RES_ID, data=RESPONSE_TELLTALE_ALL_ON)

def request_telltale_all_on(connector):
    connector.send_message(REQUEST_TELLTALE_ALL_ON, DIAG_FUN_ID)
    return None
    #return Message(arbitration_id=DIAG_RES_ID, data=RESPONSE_TELLTALE_ALL_ON)

def request_extended_session(connector):
    connector.send_message(REQUEST_EXTENDED_SESSION, DIAG_REQ_ID)
    return Message(arbitration_id=DIAG_RES_ID, data=RESPONSE_EXTENDED_SESSION)

def request_general_seed(connector):
    connector.send_message(REQUEST_GENERAL_SEED, DIAG_REQ_ID)
    return Message(arbitration_id=DIAG_RES_ID, data=RESPONSE_GENERAL_SEED)

def request_sw_version(connector):
    connector.send_message(REQUEST_SW_VERSION_READ, DIAG_REQ_ID)
    return Message(arbitration_id=DIAG_RES_ID, data=RESPONSE_GENERAL_SEED)

def request_eol_write(connector, eol_byte_1, eol_byte_2):
    write_packet = REQUEST_EOL_WRITE
    write_packet[4] = eol_byte_1
    write_packet[5] = eol_byte_2
    connector.send_message(write_packet, DIAG_REQ_ID)
    return Message(arbitration_id=DIAG_RES_ID, data=RESPONSE_EOL_WRITE)

def request_visteon_eol_write(connector, eol_byte_1, eol_byte_2, eol_byte_3, eol_byte_4):
    write_packet = REQUEST_VISTEON_EOL_WRITE
    write_packet[5] = eol_byte_1
    write_packet[6] = eol_byte_2
    write_packet[7] = eol_byte_3
    connector.send_message(write_packet, DIAG_REQ_ID)
    return Message(arbitration_id=DIAG_RES_ID, data=RESPONSE_VISTEON_EOL_WRITE)

def request_eol_read(connector):
    connector.send_message(REQUEST_EOL_READ, DIAG_REQ_ID)
    return Message(arbitration_id=DIAG_RES_ID, data=RESPONSE_EOL_READ)

def request_visteon_eol_read(connector):
    connector.send_message(REQUEST_EOL_READ_VISTEON, DIAG_REQ_ID)
    return Message(arbitration_id=DIAG_RES_ID, data=RESPONSE_EOL_READ_VISTEON)

def request_key(connector, data, is_random=False):
    key_packet = REQUEST_KEY
    if not is_random:
        key_packet[3] = data[3] ^ 0xFF
        key_packet[4] = data[4] ^ 0xFF
        key_packet[5] = data[5] ^ 0xFF
        key_packet[6] = data[6] ^ 0xFF
        key_packet[6] = key_packet[6] + 0x0D
    else:
        key_packet[3] = data[3] + 1
        key_packet[4] = data[3] + 1
        key_packet[5] = data[3] + 1
        key_packet[6] = data[3] + 1
    connector.send_message(key_packet, DIAG_REQ_ID)
    return Message(arbitration_id=DIAG_RES_ID, data=RESPONSE_KEY)

def request_key_visteon(connector, data, is_random=False):
    key_packet = REQUEST_KEY_VISTEON
    if not is_random:
        key_packet[3] = data[3] ^ 0xFF
        key_packet[4] = data[4] ^ 0xFF
        key_packet[5] = data[5] ^ 0xFF
        key_packet[6] = data[6] ^ 0xFF
        key_packet[6] = key_packet[6] + 0x0D
    else:
        key_packet[3] = data[3] + 1
        key_packet[4] = data[3] + 1
        key_packet[5] = data[3] + 1
        key_packet[6] = data[3] + 1
    connector.send_message(key_packet, DIAG_REQ_ID)
    return Message(arbitration_id=DIAG_RES_ID, data=RESPONSE_KEY_VISTEON)