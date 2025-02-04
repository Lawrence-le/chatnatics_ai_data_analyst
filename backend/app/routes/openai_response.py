from flask import Blueprint, jsonify, request
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

openai = Blueprint("openai_response", __name__)


@openai.route("/", methods=["POST"])
def get_openai_response():
    try:
        # Parse user input from the JSON request
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided in the request."}), 400

        user_input = data.get("user_input", "")

        system_response = data.get("response", "")
        if not system_response:
            return (
                jsonify({"error": "No 'response' field provided in the request."}),
                400,
            )

        # Call the OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": f"This is a response '{system_response}' from my analysis for university graduates in Singapore, with user input '{user_input}', help me rephrase to a concise yet engaging response to user, remove html styling such as strong and /n",
                },
                {"role": "user", "content": system_response},
            ],
            max_tokens=150,
        )

        # Extract the response content
        openai_response = response.choices[0].message.content

        # Return the AI response
        return jsonify({"response": openai_response}), 200

    except Exception as e:

        print(f"Error occurred: {str(e)}")

        return (
            jsonify(
                {"error": f"An error occurred while processing the request: {str(e)}"}
            ),
            500,
        )
