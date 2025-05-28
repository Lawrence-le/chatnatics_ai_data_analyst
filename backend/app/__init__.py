# app\__init__.py
from flask import Flask, Response
from flask_cors import CORS
from config.config import Config
from app.routes.data_gov_api import fetch_data_raw
from config.prompt_structure import (
    add_unique_values_column,
)


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
                    "https://chatnaticsaidataanalyst-production.up.railway.app",
                ],
                "allow_headers": ["Content-Type", "Authorization"],
            }
        },
    )

    # Fetch raw data (Pandas DataFrame)
    df_data = fetch_data_raw()

    # Convert DataFrame to dict for storage in config
    data_response = df_data.to_dict(orient="records")

    # Store it data_response in app config / global variable
    app.config["DATA_RESPONSE"] = data_response

    """
    Extract unique values for 'school' and 'degree' from the loaded dataset
    and update the 'categories' dictionary in prompt_structure accordingly.
    This ensures the keyword extractor has up-to-date lists to match user inputs against.
    """
    add_unique_values_column(data_response)

    # Import and register Blueprints
    from app.routes.user import user
    from app.routes.data_gov_api import data_gov_api
    from app.routes.get_all_data import get_all_data
    from app.routes.get_columns import get_columns
    from app.routes.openai_response import openai
    from app.routes.get_server_status import get_server_status

    app.register_blueprint(openai, url_prefix="/api/openai_response")
    app.register_blueprint(user, url_prefix="/api/user_prompt")
    app.register_blueprint(data_gov_api, url_prefix="/api/data")
    app.register_blueprint(get_columns, url_prefix="/api/get_columns")
    app.register_blueprint(get_all_data, url_prefix="/api/get_all_data")
    app.register_blueprint(get_server_status, url_prefix="/api/server_status")

    return app
