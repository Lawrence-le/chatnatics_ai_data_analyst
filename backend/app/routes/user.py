# app\routes\user.py

from flask import Blueprint, jsonify, request
import requests
from app.modules.keyword_extractor import KeywordExtractor

# from app.modules.column_mapper import ColumnMapper
from app.modules.handle_user_input import validate_user_input, handle_user_input
from config.prompt_structure import (
    categories,
    column_mapping,
    synonym_measures,
    add_unique_values_column,
)
from app.routes.data_gov_api import fetch_data
from app.modules.data_fetcher import DataFetcher


user = Blueprint("user", __name__)

keyword_extractor = KeywordExtractor(categories, synonym_measures)
# column_mapper = ColumnMapper(column_mapping)


@user.route("/prompt", methods=["POST"])
def user_prompt():
    try:
        data = request.get_json()

        print(data)

        user_input = data.get("user_input", "")

        openai_status = data.get("openai_status", "")

        # * Extract data from public api
        data_response = fetch_data().get_json()  # convert to to json

        unique_school = add_unique_values_column(data_response)

        # * Extract keywords from KeywordExtractor Class
        extracted_keywords = keyword_extractor.extract_keywords(user_input)

        # # * Extract columns from ColumnMapper Class
        # mapped_columns = column_mapper.map_to_column(extracted_keywords)

        # * Validate user_input
        validation_response = validate_user_input(extracted_keywords)

        # Check if there was a validation error, and if so, return the error response
        if validation_response:
            return jsonify(
                {
                    "process_response": validation_response,
                    "extracted_keywords": extracted_keywords,
                }
            )

        #! Prepare the successful response

        validation_response = handle_user_input(extracted_keywords, data_response)

        print("OpenAI Status:", openai_status)
        if openai_status:
            try:
                print("Running OpenAI API")
                print("validation_response:", validation_response)

                # Define the OpenAI API URL (with trailing slash)
                openai_api_url = "http://localhost:5000/api/openai_response/"

                # Prepare data for OpenAI API
                openai_request_data = {
                    "response": validation_response["response"],
                    "user_input": user_input,
                }

                # Send a POST request to the OpenAI API
                openai_api_response = requests.post(
                    openai_api_url, json=openai_request_data
                )

                # Check if the request was successful
                if openai_api_response.status_code == 200:
                    openai_response = openai_api_response.json().get("response", "")
                    print("OpenAI API Response:", openai_response)
                    if validation_response.get("charts") is None:
                        response = {
                            "user_prompt": user_input,
                            "process_response": {
                                "response": openai_response,
                            },
                        }
                    else:
                        response = {
                            "user_prompt": user_input,
                            "process_response": {
                                "response": openai_response,
                                "charts": validation_response["charts"],
                            },
                        }
                else:
                    response = {
                        "user_prompt": user_input,
                        "process_response": {
                            "response": "AI Assist is currently unavailable. Please try later or proceed without AI Assist",
                        },
                    }
                # openai_response = f"Error from OpenAI API: {openai_api_response.status_code} - {openai_api_response.text}"
                # print(openai_response)

            except requests.exceptions.RequestException as e:
                openai_response = f"Failed to connect to OpenAI API: {str(e)}"
                print(openai_response)
            except Exception as e:
                openai_response = f"An unexpected error occurred: {str(e)}"
                print(openai_response)

        else:
            # print("openai_Status", openai_status)
            response = {
                "user_prompt": user_input,
                # "extracted_keywords": extracted_keywords,
                # "mapped_columns": mapped_columns,
                # "data_response": data_response,
                "process_response": validation_response,
                # "dataset": data_response,
                # "public_data": public_data_response,
                # "add_unique_values_column": unique_school,
            }

        return jsonify(response)

    except Exception as e:
        print("Error occurred:", str(e))
        return jsonify({"error": str(e)}), 500
