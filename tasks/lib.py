from os.path import join, exists
from os import makedirs
from subprocess import run
from shutil import rmtree

from rfittools.build import (
    CMAKE_TOOLCHAIN_FILE,
    WASM_SYSROOT
)

from rfittools.env import PROJ_ROOT


def build_rfit_lib(subdir, clean=False, shared=False):
    """
    Builds one of the libraries included in this repo
    """
    work_dir = join(PROJ_ROOT, subdir)
    install_dir = WASM_SYSROOT
    build_dir = join(work_dir, "build")

    if exists(build_dir) and clean:
        rmtree(build_dir)

    makedirs(build_dir, exist_ok=True)

    extras = [
        "-DCMAKE_TOOLCHAIN_FILE={}".format(CMAKE_TOOLCHAIN_FILE),
    ]

    build_cmd = [
        "cmake",
        "-GNinja",
        "-DCMAKE_BUILD_TYPE=Release",
        "-DBUILD_SHARED_LIBS={}".format("ON" if shared else "OFF"),
        "-DCMAKE_INSTALL_PREFIX={}".format(install_dir),
    ]

    build_cmd.extend(extras)
    build_cmd.append(work_dir)

    build_cmd_str = " ".join(build_cmd)
    print(build_cmd_str)

    run(build_cmd_str, shell=True, cwd=build_dir, check=True)

    run("ninja", shell=True, cwd=build_dir, check=True)
    run("ninja install", shell=True, cwd=build_dir, check=True)
