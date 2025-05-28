# app\routes\data_gov_api.py
from flask import Blueprint, session, jsonify
import requests
import pandas as pd

data_gov_api = Blueprint("data_gov_api", __name__)


@data_gov_api.route("/", methods=["GET"])
def fetch_data():
    try:
        dataset_id = "d_3c55210de27fcccda2ed0c63fdd2b352"
        url = (
            "https://data.gov.sg/api/action/datastore_search?resource_id="
            + dataset_id
            + "&limit=2000"
        )

        response = requests.get(url)

        data = response.json()

        records = data["result"]["records"]

        df = pd.DataFrame(records)

        dataset = df.to_dict(orient="records")

        return jsonify(dataset)

    except Exception as e:
        print("Error occurred:", str(e))
        return jsonify({"error": str(e)}), 500


def fetch_data_raw():
    """
    This function fetches raw data for reuse without returning a Flask response.
    """
    dataset_id = "d_3c55210de27fcccda2ed0c63fdd2b352"
    url = (
        "https://data.gov.sg/api/action/datastore_search?resource_id="
        + dataset_id
        + "&limit=2000"
    )

    response = requests.get(url)
    data = response.json()
    records = data["result"]["records"]
    df = pd.DataFrame(records)
    return df
