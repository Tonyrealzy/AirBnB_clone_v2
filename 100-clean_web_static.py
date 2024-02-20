#!/usr/bin/python3
# Fabfile to delete out-of-date archives.

from fabric.api import env, lcd, local, run, task
import os

env.hosts = ["104.196.168.90", "35.196.46.172"]


@task
def do_clean(number=0):
    """Delete out-of-date archives.

    Args:
        number (int): The number of archives to keep.

    If number is 0 or 1, keeps only the most recent archive. If
    number is 2, keeps the most and second-most recent archives,
    etc.
    """
    number = max(int(number), 1)

    # Local clean
    with lcd("versions"):
        local("ls -1t | tail -n +{} | xargs -I {{}} rm -- {{}}"
              .format(number + 1))

    # Remote clean
    with cd("/data/web_static/releases"):
        archives = run("ls -1tr | grep 'web_static_' | tail -n +{} | xargs -I {{}} echo -- {{}}"
                       .format(number + 1)).split("-- ")
        run("rm -rf {}".format(" ".join(archives)))
