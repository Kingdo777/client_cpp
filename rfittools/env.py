from os.path import dirname, abspath, join
from multiprocessing import cpu_count

PROJ_ROOT = dirname(dirname(abspath(__file__)))
THIRD_PARTY_DIR = join(PROJ_ROOT, "third-party")
WASM_DIR = "/home/kingdo/CLionProjects/client_cpp/runtime/wasm"
RFIT_RUNTIME_ROOT = "/home/kingdo/CLionProjects/client_cpp/runtime/runtime_root"

# Environment
USABLE_CPUS = int(cpu_count()) - 1

# Versioning
VERSION_FILE = join(PROJ_ROOT, "VERSION")
LLVM_VERSION = "10.0.1"


def get_version():
    with open(VERSION_FILE) as fh:
        ver = fh.read()
    return ver.strip()
