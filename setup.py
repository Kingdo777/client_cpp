from setuptools import setup, find_packages
from os.path import join, abspath, dirname

PROJ_ROOT = dirname(abspath(__file__))

with open(join(PROJ_ROOT, "VERSION")) as fh:
    version = fh.read().strip()

setup(
    name="rfittool",
    version=version,
    packages=find_packages(),
    author="Kingdo",
    author_email="1440852110@qq.com",
    description="Utilities related to RFIT C++ functions",
    url="https://github.com/Kingdo777/client_cpp",
    python_requires=">=3.6",
)
