from invoke import task
from tasks.lib import build_rfit_lib


@task(default=True)
def build(ctx, clean=False, shared=False):
    """
    Builds rfit C/C++ lib
    """
    build_rfit_lib("librfit", clean=clean, shared=shared)
