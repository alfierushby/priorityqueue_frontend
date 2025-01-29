import os

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from prometheus_flask_exporter import PrometheusMetrics

from routes import routes

load_dotenv()

app = Flask(__name__)
# Initialize Prometheus Metrics once
metrics = PrometheusMetrics(app)

# Register blueprints
app.register_blueprint(routes)

@app.route('/',methods=["GET"])
def index():  # put application's code here
    return render_template("index.html")

@app.route('/health',methods=["GET"])
def health_check():
    """ Checks health, endpoint """
    return jsonify({"status":"healthy"}),200


if __name__ == '__main__':
    app.run(debug=False)
