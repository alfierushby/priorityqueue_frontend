import os

import boto3
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv, dotenv_values
from prometheus_flask_exporter import PrometheusMetrics

from routes import routes

load_dotenv()

def create_sqs_client(config):
    """Initialize and return a single global SQS client using app.config
    :param config: The app config in the app context
    :return: A boto3 client for sqs queries
    """
    return boto3.client(
        "sqs",
        region_name=config["AWS_REGION"],
        aws_access_key_id=config["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=config["AWS_SECRET_ACCESS_KEY"]
    )


def create_app():
    """Application factory function for testing"""
    app = Flask(__name__)

    # Store queue URLs in `app.config` for global storage
    app.config["PRIORITY_QUEUES"] = {
        "Low": os.getenv("P1_QUEUE_URL"),
        "Medium": os.getenv("P2_QUEUE_URL"),
        "High": os.getenv("P3_QUEUE_URL")
    }
    # Update app.config with needed keys directly from os.environ
    app.config["AWS_REGION"] = os.getenv("AWS_REGION")
    app.config["AWS_ACCESS_KEY_ID"] = os.getenv("AWS_ACCESS_KEY_ID")
    app.config["AWS_SECRET_ACCESS_KEY"] = os.getenv("AWS_SECRET_ACCESS_KEY")

    # Initialize and store the SQS client globally
    app.config["SQS_CLIENT"] = create_sqs_client(app.config)

    metrics = PrometheusMetrics(app)

    # Register blueprints
    app.register_blueprint(routes)

    @app.route('/', methods=["GET"])
    def index():
        return render_template("index.html")

    @app.route('/health', methods=["GET"])
    def health_check():
        """ Checks health, endpoint """
        return jsonify({"status": "healthy"}), 200

    return app


if __name__ == '__main__':
    create_app().run()
