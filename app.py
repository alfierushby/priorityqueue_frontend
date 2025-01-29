import os

from flask import Flask, render_template, request
from dotenv import load_dotenv
from routes import routes

load_dotenv()

app = Flask(__name__)
app.register_blueprint(routes)

@app.route('/',methods=["GET"])
def index():  # put application's code here
    return render_template("index.html")

if __name__ == '__main__':
    app.run()
