import os
from flask import Flask, render_template
from app.config import config


def create_app(test_config=None):
    """Create and configure the Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # Load the default config
        env = os.environ.get("FLASK_ENV", "development")
        app.config.from_object(config.get(env, config["default"]))
    else:
        # Load the test config
        app.config.from_mapping(test_config)

    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Register blueprints
    from app.routes import main

    app.register_blueprint(main.bp)

    # Register error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template("errors/500.html"), 500

    return app
