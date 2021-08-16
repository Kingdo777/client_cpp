from invoke import Collection

from . import func
from . import librfit
from . import install
from . import cpython
from . import libffi
from . import lib_rfit_python
from . import runtime

ns = Collection(
    func,
    librfit,
    install,
    cpython,
    libffi,
    lib_rfit_python,
    runtime
)
