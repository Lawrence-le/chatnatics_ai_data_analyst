# app\__init__.py
from flask import Flask, Response
from flask_socketio import SocketIO
from flask_cors import CORS
from config.config import Config

# # Initialize SocketIO and Flask App
# socketio = SocketIO(cors_allowed_origins="*")


def create_app():
    # Initialize the Flask app
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS for the app
    # CORS(app)
    CORS(
        app,
        resources={
            r"/*": {
                "origins": [
                    "http://localhost:5173",
                    "https://chatnatics-ai-data-analyst-11znfwfkh.vercel.app/",
                ]
            }
        },
    )

    # # Initialize SocketIO with app
    # socketio.init_app(app)

    # Import and register Blueprints
    # from app.routes.queries import chatgpt_queries
    from app.routes.read_reply import read_reply
    from app.routes.user import user
    from app.routes.data_gov_api import data_gov_api
    from app.routes.get_all_data import get_all_data
    from app.routes.get_columns import get_columns
    from app.routes.openai_response import openai
    from app.routes.test_openai import test_openai

    app.register_blueprint(test_openai, url_prefix="/api/test_openai")
    app.register_blueprint(openai, url_prefix="/api/openai_response")
    app.register_blueprint(read_reply, url_prefix="/api/read_reply")
    app.register_blueprint(user, url_prefix="/api/user_prompt")
    app.register_blueprint(data_gov_api, url_prefix="/api/data")
    app.register_blueprint(get_all_data, url_prefix="/api/get_all_data")
    app.register_blueprint(get_columns, url_prefix="/api/get_columns")

    return app
