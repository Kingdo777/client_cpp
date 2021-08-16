from subprocess import run

import os
from os import access
from os.path import join, exists, isfile
from shutil import copy
from invoke import task

import requests

from rfittools.env import PROJ_ROOT, RFIT_RUNTIME_ROOT
from rfittools.compile_util import wasm_cmake, wasm_copy_upload

FUNC_DIR = join(PROJ_ROOT, "func")
FUNC_BUILD_DIR = join(PROJ_ROOT, "func", "build")
PY_UPLOAD_DIR = join(RFIT_RUNTIME_ROOT, "pyfuncs", "python")
PY_FUNC_DIR = join(PROJ_ROOT, "func", "py_func")


def _copy_built_function(user, func):
    src_file = join(FUNC_BUILD_DIR, user, ".".join([func, "wasm"]))
    wasm_copy_upload(user, func, src_file)


@task(default=True, name="compile")
def compile(ctx, user, func, clean=False, debug=False):
    """
    Compile a function
    """
    # Build the function (gets written to the build dir)
    wasm_cmake(FUNC_DIR, FUNC_BUILD_DIR, func, clean, debug)

    # Copy into place
    _copy_built_function(user, func)


# /register/functionName/concurrency/core/mem
@task()
def register(ctx, user, func, concurrency, core=0, mem=0):
    """
    Register function
    """
    # func_file = join(FUNC_BUILD_DIR, "lib{}.so".format(func))
    func_file = join(FUNC_BUILD_DIR, user, ".".join([func, "wasm"]))
    if not exists(func_file):
        print("{} is not exist".format(func_file))
        return
    if not isfile(func_file):
        print("{} is not file".format(func_file))
        return
    if not access(func_file, os.R_OK):
        print("{} is nor readable".format(func_file))
        return
    url = "http://localhost:8080/register/wasm/{}/{}/{}/{}/{}".format(user, func, concurrency, core, mem)
    response = requests.put(url, data=open(func_file, "rb"))
    print("Response {}: {}".format(response.status_code, response.text))


@task()
def invoke(ctx, user, func):
    url = "http://localhost:8080/invoke/{}/{}".format(user, func)
    data = {
        "name": "Kingdo"
    }
    response = requests.post(url, json=data)
    print("Response {}:\n{}".format(response.status_code, response.text))


@task()
def hey(ctx, user, func, n, c):
    url = "http://localhost:8080/invoke/{}/{}".format(user, func)
    cmd = "hey -n {} -c {} -m POST -t 0 -d ".format(n, c) + "\"{\"name\": \"Kingdo\"}\" " + url
    print(cmd)
    res = run(cmd, shell=True)


@task()
def getRFT(ctx):
    url = "http://localhost:8080/rft/info"
    response = requests.get(url)
    print("Response Code:{}".format(response.status_code))
    print(response.text)


@task
def uploadpy(ctx, local=True):
    """
    Upload functions written in Python
    """
    if not local:
        raise RuntimeError("Remote upload not yet implemented")

    os.makedirs(PY_UPLOAD_DIR, exist_ok=True)

    # Get all Python funcs
    funcs = os.listdir(PY_FUNC_DIR)
    funcs = [f for f in funcs if f.endswith(".py")]
    funcs = [f.replace(".py", "") for f in funcs]

    for func in funcs:
        func_upload_dir = join(PY_UPLOAD_DIR, func)
        os.makedirs(func_upload_dir, exist_ok=True)

        src_file = join(PY_FUNC_DIR, "{}.py".format(func))
        dest_file = join(func_upload_dir, "function.py")
        copy(src_file, dest_file)
