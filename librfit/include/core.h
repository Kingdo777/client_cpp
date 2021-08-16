#ifndef RFITC_CORE_H
#define RFITC_CORE_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C"
{
#endif

#define BYTES(arr) reinterpret_cast<uint8_t*>(arr)

/**
 * Returns the size of the input in bytes. Returns zero if none.
 * */
long rfitGetInputSize();

/**
 * Returns a pointer to the input data for this function
 */
void rfitGetInput(uint8_t *buffer, long bufferLen);

/**
 * Sets the given array as the output data for this function
 */
void rfitSetOutput(const uint8_t *newOutput, long outputLen);

/**
 * Returns the python user
 */
char *rfitGetPythonUser();

/**
 * Returns the python function
 */
char *rfitGetPythonFunc();

/**
 * Returns the python entrypoint
 */
char *rfitGetPythonEntry();

/**
 * Returns a 1 or 0 saying whether the conf flag is on or off
 */
unsigned int getConfFlag(const char *key);

/**
 * Requests that the runtime print a backtrace for the given depth
 */
void rfitBacktrace(const int depth);


// Macro for defining zygotes (a default fallback noop is provided)
int __attribute__((weak)) _rfit_zygote();
int __attribute__((weak)) _rfit_ping_func();

#define RFIT_ZYGOTE() int _rfit_zygote()

#define RFIT_PING()   int _rfit_ping_func()

#ifdef __cplusplus
}
#endif

#endif
