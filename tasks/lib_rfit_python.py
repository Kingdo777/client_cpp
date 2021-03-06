import os

from copy import copy
from rfittools.build import WASM_LIB_INSTALL, CMAKE_TOOLCHAIN_FILE
from os.path import join
from subprocess import run
from rfittools.env import USABLE_CPUS, THIRD_PARTY_DIR, CROSSENV_DIR, PROJ_ROOT
from invoke import task, Failure

# Modified libs
MODIFIED_LIBS = {
    "pyfaasm": {
        "dir": join(PROJ_ROOT, "pyrfit"),
    },
}

MODIFIED_LIBS_ALL = copy(MODIFIED_LIBS)

# Libs that can be installed directly from PyPI
PYPI_LIBS = [
    "dulwich",
    "Genshi",
    "pyaes",
    "pyperf",
    "pyperformance",
    "six",
]


def _check_crossenv_on():
    actual = os.environ.get("VIRTUAL_ENV")
    if actual != CROSSENV_DIR:
        print(
            "Got VIRTUAL_ENV={} but expected {}".format(actual, CROSSENV_DIR)
        )
        raise Failure("Cross-env not activated")


@task
def show(ctx):
    """
    List supported libraries
    """
    print("We currently support the following libraries:")

    print("\n--- Direct from PyPI ---")
    for lib_name in PYPI_LIBS:
        print(lib_name)

    print("\n--- With modifications ---")
    for lib_name in MODIFIED_LIBS.keys():
        print(lib_name)

    print("")


@task
def install(ctx, name=None):
    """
    Install cross-compiled libraries
    """
    _check_crossenv_on()

    # Work out which modules to install
    modified_libs = dict()
    pypi_libs = list()

    if not name:
        modified_libs = MODIFIED_LIBS
        pypi_libs = PYPI_LIBS
    elif name in MODIFIED_LIBS_ALL.keys():
        modified_libs = {name: MODIFIED_LIBS_ALL[name]}
    else:
        if name not in PYPI_LIBS:
            print("WARNING: {} not definitely supported!".format(name))
        pypi_libs = [name]

    # Install modified libs
    for lib_name, lib_def in modified_libs.items():
        shell_env = copy(os.environ)
        extra_env = lib_def.get("env", {})
        shell_env.update(extra_env)

        # Work out install directory
        mod_dir = lib_def.get("dir", join(THIRD_PARTY_DIR, lib_name))
        print("Installing modified lib {} from {}".format(lib_name, mod_dir))

        # Execute the pip command
        pip_cmd = lib_def.get("pip_cmd", "pip install .")
        print(pip_cmd)
        run(pip_cmd, cwd=mod_dir, shell=True, check=True, env=shell_env)

    # Install pypi libs
    for lib_name in pypi_libs:
        print("Installing lib from PyPI {}".format(lib_name))
        run("pip install {}".format(lib_name), shell=True, check=True)
