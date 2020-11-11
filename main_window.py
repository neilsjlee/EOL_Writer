from tkinter import *
from can_connector import CANConnection
from cluster_functions import *
from hkmc_signal_functions import HKMCSignalHandler
from threading import Thread
import time
import ctypes

DEFAULT_SESSION = 0x81
EXTENDED_DIAG_SESSION = 0x03
EOL_SESSION = 0x60
PROGRAMMING_SESSION = 0x85
EXTENDED_DIAG_MODE = 0x90
cluster_session_state = 0

def set_session(session):
    result = False
    #if ui_param['session'] != session:
    if session == DEFAULT_SESSION:
        result = signal_handler.do_request("REQUEST_DEFAULT_SESSION", None)
    else:
        if session == EOL_SESSION:
            result = signal_handler.do_request("REQUEST_EOL_SESSION", None)
        if session == EXTENDED_DIAG_SESSION:
            signal_handler.do_request("REQUEST_DEFAULT_SESSION", None)
            time.sleep(0.2)
            signal_handler.do_request("REQUEST_EXTENDED_DIAG_SESSION", None)
            time.sleep(0.2)
            signal_handler.do_request("REQUEST_EXTENDED_DIAG_MODE", None)
            time.sleep(0.2)
        if session == PROGRAMMING_SESSION:
            result = signal_handler.do_request("REQUEST_PROGRAMMING_SESSION", None)

        if result:
            time.sleep(0.2)
            #result = signal_handler.do_request("REQUEST_VISTEON_SEED", None)
    return result

def send_tester_present(handler):
    while True:
        handler.do_request("REQUEST_TESTER_PRESENT")
        time.sleep(3)

def send_io_record1():
    while True:
        try:
            if ignore_status_update != True:
                signal_handler.do_request("REQUEST_IO_RECORD1")
                time.sleep(1)
        except:
            print("Error occured while sending I/O Record ")



def btn_eol_mode_on_cb(mode):
    set_session(DEFAULT_SESSION)
    if mode == DEFAULT_SESSION:
        return
    time.sleep(0.2)
    set_session(EXTENDED_DIAG_SESSION)
    if mode == EXTENDED_DIAG_SESSION:
        return
    time.sleep(0.2)
    set_session(EOL_SESSION)
    if tester_present_thread.is_alive() == False:
        tester_present_thread.start()

def eol_length_cb():
    if eol_length.get() == 2:
        customer_eol_byte3_txt.configure(state="disabled")
        customer_eol_byte4_txt.configure(state="disabled")
    else:
        customer_eol_byte3_txt.configure(state="normal")
        customer_eol_byte4_txt.configure(state="normal")

def btn_eol_write_cb():
    if security_access_setting.get() == "general_seedkey":
        result = signal_handler.do_request("REQUEST_GENERAL_SEED", None)

        if result:
            time.sleep(0.2)
            byte1 = int(eol_byte_1.get(), 16)
            byte2 = int(eol_byte_2.get(), 16)
            param = [byte1, byte2]

            if eol_length.get() == 4:
                byte3 = int(eol_byte_3.get(), 16)
                byte4 = int(eol_byte_4.get(), 16)
                param.append(byte3)
                param.append(byte4)
            signal_handler.do_request("REQUEST_EOL_WRITE", param)
        else:
            print("Request EOL Write Failure")
    elif security_access_setting.get() == "advanced_seedkey":
        result = signal_handler.do_request("REQUEST_ASK_SEED", None)

        if result:
            time.sleep(0.2)
            byte1 = int(eol_byte_1.get(), 16)
            byte2 = int(eol_byte_2.get(), 16)
            param = [byte1, byte2]

            if eol_length.get() == 4:
                byte3 = int(eol_byte_3.get(), 16)
                byte4 = int(eol_byte_4.get(), 16)
                param.append(byte3)
                param.append(byte4)
            signal_handler.do_request("REQUEST_EOL_WRITE", param)
        else:
            print("Request EOL Write Failure")

def btn_eol_read_cb():
    result = signal_handler.do_request("REQUEST_EOL_READ", None)

def btn_visteon_eol_read_cb():
    result = signal_handler.do_request("REQUEST_VISTEON_EOL_READ", None)

def btn_visteon_eol_write_cb():
    signal_handler.do_request("REQUEST_VISTEON_SEED", None)
    time.sleep(0.2)
    param = []
    param.append(int(visteon_eol_byte_1.get(), 16))
    param.append(int(visteon_eol_byte_2.get(), 16))
    param.append(int(visteon_eol_byte_3.get(), 16))
    param.append(int(visteon_eol_byte_4.get(), 16))
    signal_handler.do_request("REQUEST_VISTEON_EOL_WRITE", param)

def btn_telltale_cb():
    #request_extended_diag_mode(connection2)
    time.sleep(0.4)
    #request_telltale_all_on(connection2)

def btn_sw_reset_cb():
    set_session(EXTENDED_DIAG_SESSION)
    signal_handler.do_request("REQUEST_SW_RESET", None)
    time.sleep(3)
    on_start()

def btn_odo_reset_cb():
    set_session(EOL_SESSION)
    time.sleep(0.2)
    result = signal_handler.do_request("REQUEST_VISTEON_SEED", None)

    signal_handler.do_request("REQUEST_ODO_RESET", None)
    print("odo")

def btn_chime_test_cb(chime_index):
    signal_handler.do_request("REQUEST_VISTEON_SEED", None)
    time.sleep(0.2)
    if chime_index > 0:
        signal_handler.do_request("REQUEST_CHIME_TEST", None)
    else:
        signal_handler.do_request("REQUEST_CHIME_RELEASE", None)
 

def btn_odo_write_cb():
    #ret_msg = request_extended_session(connection)
    #time.sleep(0.2)
    #ret_msg = request_general_seed(connection)
    #time.sleep(0.4)

    #distance = int(odometer_txt.get(), 10)
    #request_write_odometer(connection, distance)

    print("odo")

def btn_pid_refresh_cb():
    #set_session(EXTENDED_DIAG_SESSION)
    #set_session(EOL_SESSION)
    #set_session(DEFAULT_SESSION)
    #time.sleep(0.2)
    #set_session(EXTENDED_DIAG_SESSION)
    #time.sleep(0.2)
    signal_handler.do_request("REQUEST_VISTEON_SEED", None)
    time.sleep(0.2)
    signal_handler.do_request("REQUEST_SUPPORTED_PID", None)
    time.sleep(0.2)
    signal_handler.do_request("REQUEST_IO_RECORD1", None)
    time.sleep(0.2)
    signal_handler.do_request("REQUEST_IO_RECORD2", None)

def btn_telltale_all_on_cb():
    #set_session(DEFAULT_SESSION)
    #time.sleep(0.2)
    #set_session(EXTENDED_DIAG_SESSION)
    #time.sleep(0.2)
    #set_session(EOL_SESSION)
    #time.sleep(0.5)
    signal_handler.do_request("REQUEST_TELLTALE_ALL_ON")

def btn_telltale_all_off_cb():
    #set_session(EOL_SESSION)
    #time.sleep(0.5)
    signal_handler.do_request("REQUEST_TELLTALE_ALL_OFF")


def btn_config_write_cb():
    print("write config")

def btn_config_read_cb():
    result = signal_handler.do_request("REQUEST_VISTEON_SEED", None)
    time.sleep(0.2)
    print("START To READ CONI")
    signal_handler.do_request("REQUEST_CONFIG_READ", None)

def on_start():
    ignore_status_update = True
    time.sleep(0.2)
    signal_handler.start()
    signal_handler.do_request("REQUEST_INTERNAL_SW_VERSION", None)
    time.sleep(0.2)
    signal_handler.do_request("REQUEST_MANUF_DATE", None)
    time.sleep(0.2)
    signal_handler.do_request("REQUEST_SW_VERSION", None)
    time.sleep(0.2)
    signal_handler.do_request("REQUEST_HW_VERSION", None)
    time.sleep(0.2)
    signal_handler.do_request("REQUEST_MMCAN_VERSION", None)
    time.sleep(0.2)
    signal_handler.do_request("REQUEST_PART_NUMBER", None)
    ignore_status_update = False
    #request_check_did_b000(connection)
    #request_read_odometer_km(connection)

def close_window():
    signal_handler.stop()
    print("TRY to quit main window")
    main_window.quit()

def load_ask_dll():
    signal_handler.load_ask_dll(ask_dll)


# Create the Main Window
ignore_status_update = False
main_window = Tk()

# Global Variables
eol_byte_1 = StringVar()
eol_byte_2 = StringVar()
eol_byte_3 = StringVar()
eol_byte_4 = StringVar()
eol_length = IntVar()

visteon_eol_byte_1 = StringVar()
visteon_eol_byte_2 = StringVar()
visteon_eol_byte_3 = StringVar()
visteon_eol_byte_4 = StringVar()
visteon_eol_byte_5 = StringVar()
visteon_eol_byte_6 = StringVar()
visteon_eol_byte_7 = StringVar()
visteon_eol_byte_8 = StringVar()

fuel = StringVar()
battery = StringVar()
odo_km = IntVar()

internal_sw_version = StringVar()
sw_version = StringVar()
hw_version = StringVar()
mmcan_version = StringVar()
part_number = StringVar()
manuf_date = StringVar()
pid = StringVar()

ui_param = {}
ui_param['internal_sw_version'] = internal_sw_version
ui_param['sw_version'] = sw_version
ui_param['hw_version'] = hw_version
ui_param['mmcan_version'] = mmcan_version
ui_param['part_number'] = part_number
ui_param['manuf_date'] = manuf_date
ui_param['pid'] = pid
ui_param['eol_byte_1'] = eol_byte_1
ui_param['eol_byte_2'] = eol_byte_2
ui_param['eol_byte_3'] = eol_byte_3
ui_param['eol_byte_4'] = eol_byte_4
ui_param['eol_length'] = eol_length
ui_param['eol_length_cb'] = eol_length_cb

ui_param['visteon_eol_byte_1'] = visteon_eol_byte_1
ui_param['visteon_eol_byte_2'] = visteon_eol_byte_2
ui_param['visteon_eol_byte_3'] = visteon_eol_byte_3
ui_param['visteon_eol_byte_4'] = visteon_eol_byte_4
ui_param['visteon_eol_byte_5'] = visteon_eol_byte_5
ui_param['visteon_eol_byte_6'] = visteon_eol_byte_6
ui_param['visteon_eol_byte_7'] = visteon_eol_byte_7
ui_param['visteon_eol_byte_8'] = visteon_eol_byte_8
ui_param['session'] = cluster_session_state

ui_param['fuel'] = fuel
ui_param['battery'] = battery
ui_param['odo_km'] = odo_km

test_input = StringVar()
ui_param['test_input'] = test_input


main_window.title("Visteon CAN Diagnostics Tool")
main_window.geometry("850x300")

signal_handler = HKMCSignalHandler(".\signals.json", ui_param, print)

tester_present_thread = Thread(target=send_tester_present,args=(signal_handler,) )
tester_present_thread.daemon = True

status_thread = Thread(target=send_io_record1)
status_thread.daemon = True
status_thread.start()

###!
security_access_setting = StringVar()
security_access_setting.set("general_seedkey")
ask_client_dll = StringVar(main_window)
ask_dll = ctypes.cdll.LoadLibrary("C:/Users/slee113/PycharmProjects/untitled/src/lib/ASK/SU2/HKMC_AdvancedSeedKey_Win32.dll")
ask_client_dll_choices = {'SU2', 'SP2'}
# ask_client_dll.set('SU2')

# Main frame
setting_frame = Frame(main_window)
status_frame = Frame(main_window)
left_frame = Frame(main_window)
contents_frame = Frame(main_window)
setting_frame.pack(side=TOP, fill=Y, anchor="w")
left_frame.pack(side=LEFT, fill=Y)
contents_frame.pack(side=LEFT, fill=Y)
status_frame.pack(side=LEFT, fill=Y, anchor="ne")

# Setting Frame
setting_label = Label(setting_frame, text="Security Settings: ")
setting_label.pack(side=LEFT, anchor="w")

Radiobutton(setting_frame, text="4 Byte Seedkey", value="general_seedkey", variable=security_access_setting, width=20).pack(side=LEFT, anchor="nw")
Radiobutton(setting_frame, text="8 Byte Seedkey", value="advanced_seedkey", variable=security_access_setting, width=20).pack(side=LEFT, anchor="nw")
OptionMenu(setting_frame, ask_client_dll, *ask_client_dll_choices).pack(side=LEFT, anchor="nw")

# Internal SW Info
version_label_frame = Frame(status_frame)
version_label_frame.pack(side=LEFT, anchor="nw")
version_info_frame = Frame(status_frame)
version_info_frame.pack(side=LEFT, anchor="ne")

label = Label(version_label_frame, text="Visteon SW Version : ")
label.pack(side=TOP)

internal_sw_version_txt = Entry(version_info_frame, width=12, textvariable=internal_sw_version)
internal_sw_version_txt.configure(state='readonly')
internal_sw_version_txt.pack(side=TOP, pady=1)

# SW Version
label = Label(version_label_frame, text="Cluster SW Version : ")
label.pack()
sw_version_txt = Entry(version_info_frame, width=12, textvariable=sw_version)
sw_version_txt.configure(state='readonly')
sw_version_txt.pack(side=TOP, pady=1)

# HW Version
label = Label(version_label_frame, text="Cluster HW Version : ")
label.pack(side=TOP)
hw_version_txt = Entry(version_info_frame, width=12, textvariable=hw_version)
hw_version_txt.configure(state='readonly')
hw_version_txt.pack(side=TOP, pady=1)

# MMCAN Version
label = Label(version_label_frame, text="MMCAN DB Version : ")
label.pack(side=TOP)
mmcan_version_txt = Entry(version_info_frame, width=12, textvariable=mmcan_version)
mmcan_version_txt.configure(state='readonly')
mmcan_version_txt.pack(side=TOP, pady=1)

# Part Number
label = Label(version_label_frame, text="Part Number : ")
label.pack(side=TOP)
part_number_txt = Entry(version_info_frame, width=12, textvariable=part_number)
part_number_txt.configure(state='readonly')
part_number_txt.pack(side=TOP, pady=1)

# Manufacturing date
label = Label(version_label_frame, text="Manuf. Date : ")
label.pack(side=TOP)
manuf_date_txt = Entry(version_info_frame, width=12, textvariable=manuf_date)
manuf_date_txt.configure(state='readonly')
manuf_date_txt.pack(side=TOP, pady=1)

# Fuel
label = Label(version_label_frame, text="Fuel(L): ")
label.pack(side=TOP)
fuel_txt = Entry(version_info_frame, width=12, textvariable=fuel)
fuel_txt.configure(state='readonly')
fuel_txt.pack(side=TOP, pady=1)

# Voltage
label = Label(version_label_frame, text="Batt(V): ")
label.pack(side=TOP)
batt_txt = Entry(version_info_frame, width=12, textvariable=battery)
batt_txt.configure(state='readonly')
batt_txt.pack(side=TOP, pady=1)

# ODO(KM)
label = Label(version_label_frame, text="Odo(km): ")
label.pack(side=TOP)
odo_km_txt = Entry(version_info_frame, width=12, textvariable=odo_km)
odo_km_txt.configure(state='readonly')
odo_km_txt.pack(side=TOP, pady=1)

refresh_btn = Button(version_info_frame, text="REFRESH", width=20, command=on_start)
refresh_btn.pack(side=TOP)

#request_btn = Button(version_info_frame, text="REQUEST", width=20, command=lambda: signal_handler.do_request("REQUEST_IO_RECORD1"))
#request_btn.pack(side=TOP)

# MODE Button
mode_frame = Frame(contents_frame)
mode_frame.pack(side=TOP, anchor="w")

eol_btn_label = Label(left_frame, text="Mode: ")
eol_btn_label.pack(side=TOP, anchor="w", pady=2)

default_mode_on_btn = Button(mode_frame, text="DEFAULT MODE", width=20, command= lambda: btn_eol_mode_on_cb(DEFAULT_SESSION))
default_mode_on_btn.pack(side=LEFT, anchor="nw")

diag_mode_on_btn = Button(mode_frame, text="DIAG MODE", width=20, command=lambda: btn_eol_mode_on_cb(EXTENDED_DIAG_SESSION))
diag_mode_on_btn.pack(side=LEFT, anchor="w")

eol_mode_on_btn = Button(mode_frame, text="EOL MODE", width=20, command=lambda: btn_eol_mode_on_cb(EOL_SESSION))
eol_mode_on_btn.pack(side=LEFT, anchor="w")

# Customer EOL
eol_frame = Frame(contents_frame)
eol_frame.pack(side=TOP, anchor="w")

eol_label = Label(left_frame, text="Customer EOL : ")
eol_label.pack(side=TOP, anchor="w", pady=2)
customer_eol_byte1_txt = Entry(eol_frame, width=4, textvariable=eol_byte_1)
customer_eol_byte1_txt.pack(side=LEFT, anchor="e", padx=5)
customer_eol_byte2_txt = Entry(eol_frame, width=4, textvariable=eol_byte_2)
customer_eol_byte2_txt.pack(side=LEFT, anchor="e", padx=5)
customer_eol_byte3_txt = Entry(eol_frame, width=4, textvariable=eol_byte_3)
customer_eol_byte3_txt.pack(side=LEFT, anchor="e", padx=5)
customer_eol_byte4_txt = Entry(eol_frame, width=4, textvariable=eol_byte_4)
customer_eol_byte4_txt.pack(side=LEFT, anchor="e", padx=5)


customer_eol_btn = Button(eol_frame, text="WRITE", width=10, command=btn_eol_write_cb)
customer_eol_btn.pack(side=LEFT, anchor="e")
customer_eol_read_btn = Button(eol_frame, text="READ", width=10, command=btn_eol_read_cb)
customer_eol_read_btn.pack(side=LEFT, anchor="e", expand=YES)

rb1 = Radiobutton(eol_frame, text="2 bytes", variable=eol_length, value=2, command=eol_length_cb)
rb2 = Radiobutton(eol_frame, text="4 bytes", variable=eol_length, value=4, command=eol_length_cb)
rb1.pack(side=LEFT, anchor="e")
rb2.pack(side=LEFT, anchor="e")
eol_length.set(2)
eol_length_cb()

# VISTEON EOL
visteon_eol_frame = Frame(contents_frame)
visteon_eol_frame.pack(side=TOP, anchor="w")

label = Label(left_frame, text="Visteon EOL : ")
label.pack( side=TOP, anchor="w", pady=2)

visteon_eol_byte1_txt = Entry(visteon_eol_frame, width=4, textvariable=visteon_eol_byte_1)
visteon_eol_byte1_txt.pack(side=LEFT, anchor="e",  padx=5)

visteon_eol_byte2_txt = Entry(visteon_eol_frame, width=4, textvariable=visteon_eol_byte_2)
visteon_eol_byte2_txt.pack(side=LEFT, anchor="e", padx=5)
visteon_eol_byte3_txt = Entry(visteon_eol_frame, width=4, textvariable=visteon_eol_byte_3)
visteon_eol_byte3_txt.pack(side=LEFT, anchor="e",  padx=5)

visteon_eol_byte4_txt = Entry(visteon_eol_frame, width=4, textvariable=visteon_eol_byte_4)
visteon_eol_byte4_txt.pack(side=LEFT, anchor="e",  padx=5)

visteon_eol_byte5_txt = Entry(visteon_eol_frame, width=4, textvariable=visteon_eol_byte_5)
visteon_eol_byte5_txt.pack(side=LEFT, anchor="e", padx=5)

visteon_eol_byte6_txt = Entry(visteon_eol_frame, width=4, textvariable=visteon_eol_byte_6)
visteon_eol_byte6_txt.pack(side=LEFT, anchor="e",  padx=5)

visteon_eol_byte7_txt = Entry(visteon_eol_frame, width=4, textvariable=visteon_eol_byte_7)
visteon_eol_byte7_txt.pack(side=LEFT, anchor="e", padx=5)

visteon_eol_byte8_txt = Entry(visteon_eol_frame, width=4, textvariable=visteon_eol_byte_8)
visteon_eol_byte8_txt.pack(side=LEFT, anchor="e", padx=5)

visteon_eol_btn = Button(visteon_eol_frame, text="WRITE", width=10, command=btn_visteon_eol_write_cb)
visteon_eol_btn.pack(side=LEFT, anchor="e")

visteon_eol_read_btn = Button(visteon_eol_frame, text="READ", width=10, command=btn_visteon_eol_read_cb)
visteon_eol_read_btn.pack(side=LEFT, anchor="e")

# I/O Monitoring
'''io_mon_frame = Frame(contents_frame)
io_mon_frame.pack(side=TOP, anchor="w")

label = Label(left_frame, text="SUPPORTED PID : ")
label.pack(side=TOP, anchor="w", pady=2)

pid_txt = Entry(io_mon_frame, width=10, textvariable=pid)
pid_txt.pack(side=LEFT, anchor="e",  padx=5)

pid_write_read_btn = Button(io_mon_frame, text="REFRESH", width=10, command=btn_pid_refresh_cb)
pid_write_read_btn.pack(side=LEFT)


# ODOMETER
odo_frame = Frame(contents_frame)
odo_frame.pack(side=TOP, anchor="w")

label = Label(left_frame, text="ODOMETER : ")
label.pack(side=TOP, anchor="w", pady=5)

odometer_txt = Entry(odo_frame, width=10, textvariable=odometer)
odometer_txt.pack(side=LEFT, anchor="e",  padx=5)

odo_write_btn = Button(odo_frame, text="WRITE", width=10, command=btn_odo_write_cb)
odo_write_btn.pack(side=LEFT)
odo_write_read_btn = Button(odo_frame, text="READ", width=10, command=btn_odo_write_cb)
odo_write_read_btn.pack(side=LEFT)'''

label = Label(left_frame, text=" FUNCTIONS : ")
label.pack(side=TOP, anchor="w", pady=5)

func_frame = Frame(contents_frame)
func_frame.pack(side=TOP, anchor="w")

sw_reset_btn = Button(func_frame, text="S/W RESET", width=10, command=btn_sw_reset_cb)
sw_reset_btn.pack(side=LEFT)

sw_reset_btn = Button(func_frame, text="H/W RESET", width=10, command=lambda: signal_handler.do_request("REQUEST_HW_RESET"))
sw_reset_btn.pack(side=LEFT)


tt_all_on_btn = Button(func_frame, text="TT_ALL_ON", width=10, command=btn_telltale_all_on_cb)
tt_all_on_btn.pack(side=LEFT)

tt_all_off_btn = Button(func_frame, text="TT_ALL_OFF", width=10, command=btn_telltale_all_off_cb)
tt_all_off_btn.pack(side=LEFT)

gauge_sweep_btn = Button(func_frame, text="GAUGE SWEEP", width=15, command=lambda: signal_handler.do_request("REQUEST_GAUGE_SWEEP"))
gauge_sweep_btn.pack(side=LEFT)


label = Label(left_frame, text=" CHIME : ")
label.pack(side=TOP, anchor="w")
chime_frame = Frame(contents_frame)
chime_frame.pack(side=TOP, anchor="w")
chime_test_btn = Button(chime_frame, text="CHIME_ON", width=20, command=lambda: btn_chime_test_cb(1))
chime_test_btn.pack(side=LEFT)

chime_test_btn = Button(chime_frame, text="CHIME_OFF", width=20, command=lambda: btn_chime_test_cb(0))
chime_test_btn.pack(side=LEFT)





'''
config_txt = Entry(contents_frame, width=10, textvariable=config)
config_txt.pack(padx=5)

config_write_btn = Button(contents_frame, text="WRITE", width=10, command=btn_config_write_cb)
config_write_btn.pack()

config_read_btn = Button(contents_frame, text="READ", width=10, command=btn_config_read_cb)
config_read_btn.pack()

telltale_btn = Button(contents_frame, text="TELLTALE ALL ON", width=20, command=btn_telltale_cb)
telltale_btn.pack()


odometer_reset_btn = Button(contents_frame, text="ODOMETER RESET", width=20, command=btn_odo_reset_cb)
odometer_reset_btn.pack()

chime_test_btn = Button(contents_frame, text="CHIME_TEST", width=20, command=btn_chime_test_cb)
chime_test_btn.pack()

customer_eol_byte1_txt = Entry(contents_frame, width=4, textvariable=test_input)
customer_eol_byte1_txt.pack(  padx=5)'''




main_window.after(100, on_start)
main_window.protocol("WM_DELETE_WINDOW", close_window)
main_window.mainloop()
