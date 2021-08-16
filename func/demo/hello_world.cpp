#include <rfit/rfit.h>
#include <cstdint>

RFIT_PING() { return 777; }

RFIT_ZYGOTE() { return 0; }

int main() {
    char out[] = "Hello WASM\n";
    rfitSetOutput((uint8_t *) out, sizeof(out));
    return 0;
}
