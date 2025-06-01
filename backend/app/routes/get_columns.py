# app\routes\get_columns.py
from flask import Blueprint, jsonify
from app.routes.data_gov_api import fetch_data_raw


get_columns = Blueprint("get_columns", __name__)


@get_columns.route("/", methods=["GET"])
def fetch_data():
    try:

        # * Extract data from public api
        df = fetch_data_raw()  # convert to to json

        # Columns to exclude
        excluded_columns = [
            "_id",
            "employment_rate_overall",
            "employment_rate_ft_perm",
            "basic_monthly_mean",
            "basic_monthly_median",
            "gross_monthly_mean",
            "gross_monthly_median",
            "gross_mthly_25_percentile",
            "gross_mthly_75_percentile",
        ]

        # Create a dictionary to store unique values
        unique_values = {}

        # Iterate over columns and extract unique values for allowed columns
        for column in df.columns:
            if column not in excluded_columns:
                unique_values[column] = df[column].dropna().unique().tolist()

        # Return the unique values as a JSON response
        return jsonify({"unique_values": unique_values})

    except Exception as e:
        print("Error occurred:", str(e))
        return jsonify({"error": str(e)}), 500
