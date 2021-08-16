#include <rfit/rfit.h>

RFIT_PING() { return 777; }

int main() {
    auto size = rfitGetInputSize();
    return 0;
}
