from flask import Flask, request, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Survey, Question

app = Flask(__name__)
app.config['SECRET_KEY'] = "debugkey"

debug = DebugToolbarExtension(app)


responses = []

@app.route("/")
def home_page():
    return render_template('base.html')