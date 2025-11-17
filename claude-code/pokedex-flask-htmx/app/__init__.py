import os
from flask import Flask
from app.config import config


def create_app(test_config=None):
    """Create and configure the Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # Load the default config
        env = os.environ.get('FLASK_ENV', 'development')
        app.config.from_object(config.get(env, config['default']))
    else:
        # Load the test config
        app.config.from_mapping(test_config)

    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app
