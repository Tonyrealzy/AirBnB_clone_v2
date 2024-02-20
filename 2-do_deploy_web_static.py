#!/usr/bin/python3
# Fabfile to distribute an archive to a web server.

from fabric.api import env, put, run, task
from fabric.main import main
from os.path import isfile

env.hosts = ["104.196.168.90", "35.196.46.172"]


@task
def do_deploy(archive_path):
    """Distributes an archive to a web server.

    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        If the file doesn't exist at archive_path or an error occurs - False.
        Otherwise - True.
    """
    if not isfile(archive_path):
        return False

    file_name = archive_path.split("/")[-1]
    name = file_name.split(".")[0]
    tmp_archive_path = "/tmp/{}".format(file_name)

    # Upload archive to /tmp directory on the server
    if put(archive_path, tmp_archive_path).failed:
        return False

    # Create necessary directories and extract archive
    commands = [
        "rm -rf /data/web_static/releases/{}/".format(name),
        "mkdir -p /data/web_static/releases/{}/".format(name),
        "tar -xzf {} -C /data/web_static/releases/{}/".format(tmp_archive_path,
                                                              name),
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
