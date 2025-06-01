# app\routes\get_all_data.py
from flask import Blueprint, session, jsonify

get_all_data = Blueprint("get_all_data", __name__)


@get_all_data.route("/", methods=["GET"])
def fetch_data():
    try:
        return jsonify(
            {
                "session_data": session.get("user_input"),
            }
        )

    except Exception as e:
        print("Error occurred:", str(e))
        return jsonify({"error": str(e)}), 500
