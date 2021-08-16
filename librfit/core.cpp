#include "core.h"

extern "C"
{
#include "host_interface.h"
}

long rfitGetInputSize() {
    uint8_t buf[1];
    // Passing zero buffer len returns total size
    return __rfit_read_input(buf, 0);
}

void rfitGetInput(uint8_t *buffer, long bufferLen) {
    __rfit_read_input(buffer, bufferLen);
}

void rfitSetOutput(const uint8_t *newOutput, long outputLen) {
    __rfit_write_output(newOutput, outputLen);
}

char* rfitGetPythonUser()
{
    char* user = new char[20];
    __rfit_get_py_user(BYTES(user), 20);
    return user;
}

char* rfitGetPythonFunc()
{
    char* funcName = new char[20];
    __rfit_get_py_func(BYTES(funcName), 20);
    return funcName;
}

char* rfitGetPythonEntry()
{
    char* entryFuncName = new char[30];
    __rfit_get_py_entry(BYTES(entryFuncName), 30);
    return entryFuncName;
}

unsigned int getConfFlag(const char* key)
{
    return __rfit_conf_flag(key);
}
