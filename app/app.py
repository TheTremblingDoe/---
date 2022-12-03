#!/usr/bin/env python

from flask import Flask           # import flask
app = Flask(__name__)             # create an app instance

BATTERY_CHARGE = 100
MIXTURE_LEVEL = 100
BASE_POSITION = ["x1", "y1", "z1"]

@app.route("/")                   # at the end point /
def hello():                      # call method hello
    return f"Hello World! Base coordinates: {BASE_POSITION[0], BASE_POSITION[1], BASE_POSITION[2]}"         # which returns "hello world" and version number
if __name__ == "__main__":        # on running python app.py
    app.run(host="0.0.0.0")