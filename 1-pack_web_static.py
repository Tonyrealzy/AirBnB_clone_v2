#!/usr/bin/python3
# Fabfile to generate a .tgz archive from the contents of web_static.

import os
from datetime import datetime
from fabric.api import local, task


@task
def do_pack():
    """Create a tar gzipped archive of the directory web_static."""
    dt = datetime.utcnow()
    formatted_time = dt.strftime("%Y%m%d%H%M%S")
    file_name = f"versions/web_static_{formatted_time}.tgz"

    # Create 'versions' directory if it doesn't exist
    os.makedirs("versions", exist_ok=True)

    # Use f-strings for better readability
    if local(f"tar -cvzf {file_name} web_static").failed:
        return None

    return file_name
