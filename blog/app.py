from time import time

from flask import Flask, g, request

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello you are at index html!"


@app.route("/user/")
def read_user():
    name = request.args.get("name")
    surname = request.args.get("surname")
    return f"User {name or '[no name]'} {surname or '[no surname]'}"


@app.before_request
def process_before_request():
    """
    Sets start_time to `g` object
    """
    g.start_time = time()


@app.after_request
def process_after_request(response):
    """
    adds process time in headers
    """
    if hasattr(g, "start_time"):
        response.headers["process-time"] = time() - g.start_time
    return response


@app.errorhandler(404)
def page_not_found(error):
    return f"<h1>Wrong page!</h1> <br> {error}", 404
