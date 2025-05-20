# app\__init__.py
from flask import Flask, Response
from flask_cors import CORS
from config.config import Config


def create_app():

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
                    "https://chatnatics-ai-data-analyst.vercel.app",
                    "https://chatnaticsaidataanalyst-production.up.railway.app/",
                ],
                "allow_headers": ["Content-Type", "Authorization"],
            }
        },
    )

    # Import and register Blueprints
    # from app.routes.queries import chatgpt_queries
    from app.routes.read_reply import read_reply
    from app.routes.user import user
    from app.routes.data_gov_api import data_gov_api
    from app.routes.get_all_data import get_all_data
    from app.routes.get_columns import get_columns
    from app.routes.openai_response import openai
    from app.routes.test_openai import test_openai
    from app.routes.get_server_status import get_server_status

    app.register_blueprint(test_openai, url_prefix="/api/test_openai")
    app.register_blueprint(openai, url_prefix="/api/openai_response")
    app.register_blueprint(read_reply, url_prefix="/api/read_reply")
    app.register_blueprint(user, url_prefix="/api/user_prompt")
    app.register_blueprint(data_gov_api, url_prefix="/api/data")
    app.register_blueprint(get_columns, url_prefix="/api/get_columns")

    app.register_blueprint(get_all_data, url_prefix="/api/get_all_data")
    app.register_blueprint(get_server_status, url_prefix="/api/server_status")

    return app
