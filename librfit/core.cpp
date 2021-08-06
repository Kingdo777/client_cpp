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