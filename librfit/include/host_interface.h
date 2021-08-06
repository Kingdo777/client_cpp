#ifndef RFIT_HOST_INTERFACE_H
#define RFIT_HOST_INTERFACE_H

#ifdef __wasm__
#define HOST_IFACE_FUNC
#else
//#define HOST_IFACE_FUNC __attribute__((weak))
#define HOST_IFACE_FUNC
#endif

HOST_IFACE_FUNC
long __rfit_read_input(unsigned char *buffer, long bufferLen);

HOST_IFACE_FUNC
void __rfit_write_output(const unsigned char *output, long outputLen);

#endif
