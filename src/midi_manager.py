import mido

open_ports = []

def get_input_port_names():
    return mido.get_input_names()

def get_output_port_names():
    return mido.get_output_names()

def get_input_port(device_name):
    return mido.open_input(device_name.strip())

def get_output_port(device_name):
    return mido.open_output(device_name.strip())

def close_open_ports():
    for port in open_ports:
        port.close()