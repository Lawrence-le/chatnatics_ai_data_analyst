# app/routes/read_reply.py
from flask import Blueprint, jsonify, session

read_reply = Blueprint('read_reply', __name__)


@read_reply.route('/get_keywords', methods=['GET'])
def get_keywords():
    # Retrieve keywords from the session
    keywords = session.get('keywords', None)

    if keywords:
        print(session)  # Print the session to see what it contains

        return jsonify({"keywords": keywords}), 200
    else:
        print('error:', session)  # Print the session to see what it contains

        return jsonify({"error": "No keywords found in session"}), 404