#!/usr/bin/python3
# Fabfile to create and distribute an archive to a web server.

from fabric.api import env, local, put, run, task
from datetime import datetime
import os

env.hosts = ["104.196.168.90", "35.196.46.172"]


@task
def do_pack():
    """Create a tar gzipped archive of the directory web_static."""
    dt = datetime.utcnow()
    file_name = "versions/web_static_{}{}{}{}{}{}.tgz".format(dt.year,
                                                              dt.month,
                                                              dt.day,
                                                              dt.hour,
                                                              dt.minute,
                                                              dt.second)
    if not os.path.isdir("versions"):
        local("mkdir -p versions")

    if local("tar -cvzf {} web_static".format(file_name)).failed:
        return None

    return file_name


@task
def do_deploy(archive_path):
    """Distribute an archive to a web server."""
    if not os.path.isfile(archive_path):
        return False

    file_name = os.path.basename(archive_path)
    name = os.path.splitext(file_name)[0]

    tmp_archive_path = "/tmp/{}".format(file_name)

    # Upload archive to /tmp directory on the server
    if put(archive_path, tmp_archive_path).failed:
        return False

    # Create necessary directories and extract archive
    commands = [
        "rm -rf /data/web_static/releases/{}/".format(name),
        "mkdir -p /data/web_static/releases/{}/".format(name),
        "tar -xzf {} -C /data/web_static/releases/{}/"
        .format(tmp_archive_path, name),
        "rm {}".format(tmp_archive_path),
        "mv /data/web_static/releases/{}/web_static/*"
        "/data/web_static/releases/{}/"
        .format(name, name),
        "rm -rf /data/web_static/releases/{}/web_static".format(name),
        "rm -rf /data/web_static/current",
        "ln -s /data/web_static/releases/{}/ /data/web_static/current"
        .format(name)
    ]

    # Execute commands on the server
    for command in commands:
        if run(command).failed:
            return False

    return True


@task
def deploy():
    """Create and distribute an archive to a web server."""
    file = do_pack()
    if file is None:
        return False
    return do_deploy(file)
