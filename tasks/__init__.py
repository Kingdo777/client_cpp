from invoke import Collection

from . import func
from . import librfit
from . import install

ns = Collection(
    func,
    librfit,
    install
)
