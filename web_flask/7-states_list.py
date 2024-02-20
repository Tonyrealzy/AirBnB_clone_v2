#!/usr/bin/python3
"""Flask Web Application for State Information.

This script starts a Flask web application that provides a list of all State objects.
The application listens on 0.0.0.0, port 5000.

Routes:
    /states_list: Displays an HTML page with a list of all State objects in DBStorage.
"""

from models import storage
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/states_list", strict_slashes=False)
def states_list():
    """Display an HTML page with a list of all State objects in DBStorage.

    States are sorted by name.

    Returns:
        str: Rendered HTML page.

    """
    states = storage.all("State")
    return render_template("7-states_list.html", states=states)


@app.teardown_appcontext
def teardown(exc):
    """Remove the current SQLAlchemy session."""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
