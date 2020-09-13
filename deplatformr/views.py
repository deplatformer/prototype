from flask import Flask, render_template
from deplatformr import app


@app.route("/")
def homepage():
    return render_template("index.html")
