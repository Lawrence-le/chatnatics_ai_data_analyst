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

        # headers = df.columns.tolist()

        # return jsonify(
        #     {
        #         "df_headers": headers,
        #     }
        # )
        return jsonify(dataset)

    except Exception as e:
        print("Error occurred:", str(e))
        return jsonify({"error": str(e)}), 500

    # return jsonify(
    #     {"mean_basic_monthly_nus": mean_basic_monthly_nus, "session_data": session_data}
    # )


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


"""
def print_lines(records):
    for record in records:  # Iterate through the list of dictionaries
        for key, value in record.items():
            print(f"  {key}: {value}")
        print("=" * 40)


print(print_lines(records))
"""

"""
### PANDAS

        # Convert "basic_monthly_mean" to numeric, if necessary
        df["basic_monthly_mean"] = pd.to_numeric(
            df["basic_monthly_mean"], errors="coerce"
        )
        mean_basic_monthly = round(df["basic_monthly_mean"].mean())

        # Filter the DataFrame where the university is "National University of Singapore"
        nus_df = df[df["university"] == "National University of Singapore"]

        # Filter the DataFrame where the university is "National University of Singapore"
        sutd_df = df[
            df["university"] == "Singapore University of Technology and Design"
        ]

        # Calculate the mean of "basic_monthly_mean" for the filtered DataFrame
        mean_basic_monthly_nus = round(nus_df["basic_monthly_mean"].mean())

        # Calculate the mean of "basic_monthly_mean" for the filtered DataFrame
        mean_basic_monthly_sutd = round(sutd_df["basic_monthly_mean"].mean())

        """
