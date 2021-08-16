import os
import ctypes

env_cache = dict()

input_data = None
output_data = None

_host_interface = None


def get_env_bool(var_name):
    global env_cache

    if var_name not in env_cache:
        value = os.environ.get(var_name)
        env_cache[var_name] = bool(value)

    return env_cache[var_name]


def set_env_bool(var_name, value):
    global env_cache
    env_cache[var_name] = value


def _init_host_interface():
    global _host_interface
    if _host_interface is None:
        # Wasm expects the main application to handle the relevant calls
        _host_interface = ctypes.CDLL(None)


def get_input_len():
    _init_host_interface()
    return _host_interface.__rfit_read_input(None, 0)


def read_input(input_len):
    _init_host_interface()
    input_len = int(input_len)
    buff = ctypes.create_string_buffer(input_len)
    _host_interface.__rfit_read_input(buff, input_len)
    return buff.value


def write_output(output):
    _init_host_interface()
    _host_interface.__rfit_write_output(output, len(output))
