from subprocess import run

# 这里一定要这样写成 rfittools.build 而不能是 build， 否则其他的package无法引用
from rfittools.build import CMAKE_TOOLCHAIN_FILE
from rfittools.env import WASM_DIR

from os import makedirs
from os.path import join, exists
from shutil import copy, rmtree


def wasm_cmake(src_dir, build_dir, target, clean=False, debug=False):
    build_type = "wasm"
    cmake_build_type = "Debug" if debug else "Release"

    if exists(build_dir) and clean:
        rmtree(build_dir)

    makedirs(build_dir, exist_ok=True)

    build_cmd = [
        "cmake",
        "-GNinja",
        "-DRFIT_BUILD_TYPE={}".format(build_type),
        "-DCMAKE_TOOLCHAIN_FILE={}".format(CMAKE_TOOLCHAIN_FILE),
        "-DCMAKE_BUILD_TYPE={}".format(cmake_build_type),
        src_dir,
    ]

    build_cmd = " ".join(build_cmd)
    print(build_cmd)

    res = run(build_cmd, shell=True, cwd=build_dir)
    if res.returncode != 0:
        raise RuntimeError("Failed on cmake for {}".format(target))

    cmd = "ninja -vv" if debug else "ninja"
    cmd = "{} {}".format(cmd, target) if target else cmd
    res = run(cmd, shell=True, cwd=build_dir)

    if res.returncode != 0:
        raise RuntimeError("failed on make for {}".format(target))


def wasm_copy_upload(user, func, wasm_file):
    dest_folder = join(WASM_DIR, user, func)

    makedirs(dest_folder, exist_ok=True)
    dest_file = join(dest_folder, "function.wasm")

    copy(wasm_file, dest_file)


if __name__ == '__main__':
    print(CMAKE_TOOLCHAIN_FILE)
