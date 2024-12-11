from flask import Flask

app = Flask("She Moves")

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>" 