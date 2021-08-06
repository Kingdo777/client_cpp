from subprocess import run

import os
from os import access
from os.path import join, exists, isfile

from invoke import task

import requests

from rfittools.env import PROJ_ROOT
from rfittools.compile_util import wasm_cmake, wasm_copy_upload

FUNC_DIR = join(PROJ_ROOT, "func")
FUNC_BUILD_DIR = join(PROJ_ROOT, "func", "build")


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
@task(default=True)
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
    if func == "hello1":
        core = 0.5
        mem = 128
    url = "http://localhost:8080/register/{}/{}/{}/{}".format(func, concurrency, core, mem)
    response = requests.put(url, data=open(func_file, "rb"))
    print("Response {}: {}".format(response.status_code, response.text))


@task()
def invoke(ctx, func):
    url = "http://localhost:8080/invoke/{}".format(func)
    data = {
        "name": "Kingdo"
    }
    response = requests.post(url, json=data)
    print("Response {}:\n{}".format(response.status_code, response.text))


@task()
def hey(ctx, func, n, c):
    url = "http://localhost:8080/invoke/{}".format(func)
    cmd = "hey -n {} -c {} -m POST -t 0 -d ".format(n, c) + "\"{\"name\": \"Kingdo\"}\" " + url
    print(cmd)
    res = run(cmd, shell=True)


@task()
def getRFT(ctx):
    url = "http://localhost:8080/rft/info"
    response = requests.get(url)
    print("Response Code:{}".format(response.status_code))
    print(response.text)
