#!/usr/bin/python3
"""Flask Web Application for State Information.

This script starts a Flask web application that provides information about States.
The application listens on 0.0.0.0, port 5000.

Routes:
    /states: Displays an HTML page with a list of all State objects sorted by name.
    /states/<id>: Displays an HTML page with information about the State with the given <id>.

Requirements:
    - Flask: You can install it using `pip install Flask`.
    - models: Ensure the 'models' module is available with the necessary 'State' class.

Usage:
    Run this script to start the Flask web application.

Author:
    Your Name

"""

from models import storage
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/states", strict_slashes=False)
def states():
    """Display an HTML page with a list of all States.

    States are sorted by name.

    Returns:
        str: Rendered HTML page.

    """
    states = storage.all("State")
    return render_template("9-states.html", state=states)


@app.route("/states/<id>", strict_slashes=False)
def states_id(id):
    """Display an HTML page with information about the State with the given <id>.

    Args:
        id (str): The ID of the State to display.

    Returns:
        str: Rendered HTML page.

    """
    for state in storage.all("State").values():
        if state.id == id:
            return render_template("9-states.html", state=state)
    return render_template("9-states.html")


@app.teardown_appcontext
def teardown(exc):
    """Remove the current SQLAlchemy session."""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
