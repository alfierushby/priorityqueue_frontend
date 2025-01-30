import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv, dotenv_values
from prometheus_flask_exporter import PrometheusMetrics

from routes import routes

load_dotenv()

def create_app(testing=False):
    """Application factory function for testing"""
    app = Flask(__name__)
    app.config["TESTING"] = testing  # Enable testing mode if needed

    # Store queue URLs in `app.config` for global storage
    app.config["PRIORITY_QUEUES"] = {
        "Low": os.getenv("P1_QUEUE_URL"),
        "Medium": os.getenv("P2_QUEUE_URL"),
        "High": os.getenv("P3_QUEUE_URL")
    }
    # Set all env variables to the config so no mix usage is done. Always use app.config!
    config = dotenv_values()
    app.config.from_mapping(config)

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
    create_app().run(debug=False)
