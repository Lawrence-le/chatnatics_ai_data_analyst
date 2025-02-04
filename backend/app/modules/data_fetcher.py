import requests
import pandas as pd


class DataFetcher:
    def __init__(self, base_url, dataset_id, limit):
        """
        Initialize the DataFetcher with the base URL, dataset ID, and limit.

        :param base_url: The base URL for the API.
        :param dataset_id: The dataset ID to fetch data from.
        :param limit: The maximum number of records to fetch (default is 2000).
        """
        self.base_url = base_url
        self.dataset_id = dataset_id
        self.limit = limit

    def fetch(self):

        try:
            # Construct the full URL
            full_url = f"{self.base_url}{self.dataset_id}{self.limit}"
            response = requests.get(full_url)

            # Parse the JSON response
            data = response.json()

            # Extract records
            records = data["result"]["records"]  # This is a list of dictionaries

            # Convert the records to a DataFrame
            df = pd.DataFrame(records)

            # Serialize the DataFrame to a JSON-serializable format
            return df.to_dict(orient="records")  # Convert to a list of dictionaries

        except requests.RequestException as e:
            raise ValueError(f"HTTP request failed: {e}")
        except Exception as e:
            raise ValueError(f"An error occurred while fetching data: {e}")
