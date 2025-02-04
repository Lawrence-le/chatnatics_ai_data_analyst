from flask import Flask, request, jsonify, Blueprint
from openai import OpenAI
import os


test_openai = Blueprint("test_openai", __name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@test_openai.route("/generate", methods=["POST"])
def generate_text():

    user_input = request.json.get("response", "")

    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    try:

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "This is a response from my analysis, help me rephrase to a concise yet engaging response to user and keeping the html styling",
                },
                {"role": "user", "content": user_input},
            ],
            max_tokens=150,
        )

        openai_response = response.choices[0].message.content

        return jsonify({"response": openai_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
