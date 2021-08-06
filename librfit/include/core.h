#ifndef RFITC_CORE_H
#define RFITC_CORE_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C"
{
#endif
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

#ifdef __cplusplus
}
#endif

#endif
