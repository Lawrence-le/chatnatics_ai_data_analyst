from flask import Blueprint, session, jsonify
import requests
import pandas as pd

get_server_status = Blueprint("get_server_status", __name__)

@get_server_status.route("/", methods=["GET"])
def check_server_status():
    try:
        # Simple server status check response
        return jsonify({"status": "server is up and running"}), 200
    except Exception as e:
        print("Error occurred:", str(e))
        return jsonify({"error": str(e)}), 500