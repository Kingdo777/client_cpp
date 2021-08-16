try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

PKG_NAME = "pyrfit"


def main():
    long_description = """
## Rfit Python Bindings
See main repo at https://github.com/Kingdo777/RFIT
    """
    setup(
        name=PKG_NAME,
        packages=[PKG_NAME],
        version="0.0.1",
        description="Python interface for RFIT",
        long_description=long_description,
        long_description_content_type="text/markdown",
        author="Simon S",
        author_email="foo@bar.com",
        url="https://github.com/Kingdo777/client_cpp",
    )


if __name__ == "__main__":
    main()
