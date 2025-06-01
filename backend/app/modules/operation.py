# app\modules\operation.py
import base64
import io
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np

# from app.routes.data_gov_api import fetch_data
# from app.modules.data_fetcher import DataFetcher
# from flask import Flask, send_file


class CheckOperation:

    def __init__(self, extracted_keywords):
        self.input_keywords = extracted_keywords
        self.operation = extracted_keywords.get("operation", None)

    def check(self):

        if self.operation:
            return

        else:
            return {
                "response": "Please provide your intended operation. I currently support Predict, Calculate"
            }


class CheckYear:

    def __init__(self, extracted_keywords):
        self.input_keywords = extracted_keywords
        self.year = extracted_keywords.get("year", None)
        self.operation = extracted_keywords.get("operation", None)

    def check(self):

        # if self.year is None:
        if not self.year or len(str(self.year)) == 0:
            return {
                "response": "The year is required, and currently, I do not support a range of years."
            }

        self.year = int(self.year)
        if self.year < 2013:
            return {"response": "Please select a year from 2013 or later."}

        # Skip this check if the operation is 'predict'
        if self.operation != "predict" and self.year > 2023:
            return {"response": "The current data only supports up to 2022."}

        # If validation passes
        return None


class CheckMeasures:

    def __init__(self, extracted_keywords):
        self.input_keywords = extracted_keywords
        self.measures = extracted_keywords.get(
            "measure", None
        )  # Check for the "measure" key

    def check(self):

        # If there is no measure provided, return an error message
        if self.measures is None:
            return {
                "response": "The measure is required. Example: salary, wages, mean, median, etc.."
            }

        # Check if the measure is specifically "salary"
        if self.measures == "salary":
            return None  # Validation passes if "salary" is found


class CheckEntity:

    def __init__(self, extracted_keywords):
        self.input_keywords = extracted_keywords
        self.degree = extracted_keywords.get("degree", None)
        self.university = extracted_keywords.get("university", None)
        self.school = extracted_keywords.get("school", None)

    def check(self):

        print("Degree:", self.degree)
        print("School:", self.school)
        print("University:", self.university)

        # Only fail validation if all three are None
        if all(value is None for value in [self.degree, self.university, self.school]):
            return {
                "response": "Please provide at least one of the following: degree, university, or school."
            }

        # If validation passes
        return None


class FilterEntity:

    def __init__(self, data, degree, university, school, year, predict=False):
        """Initialize with data and optional entity filters (degree, university, school)."""
        self.data = data
        self.degree = degree
        self.university = university
        self.school = school
        self.year = year
        self.predict = predict  # New parameter to allow prediction logic

    def apply_filters(self):
        """Apply the filters based on degree, university, and school."""

        # Start with the full dataset
        filtered_data = self.data

        df = pd.DataFrame(filtered_data)

        # Check the first 3 characters of each column value and convert if they are numeric

        for column in df.columns:
            # Check if the first character of any value in the column is a digit (excluding NaN)
            if (
                df[column]
                .apply(lambda x: str(x)[0].isdigit() if pd.notna(x) else False)
                .any()
            ):
                # Convert the entire column to numeric
                df[column] = pd.to_numeric(df[column], errors="coerce")

        # Drop rows with NaN values after conversion
        df = df.dropna()

        # * Apply filter with provided keyword: university, degree, school, and year
        if self.university or self.degree or self.school or self.year:
            conditions = []
            filter_messages = []

            if "year" in df.columns:
                df["year"] = df["year"].fillna("").astype(str)

            # Filter by university
            if self.university:
                # print("Applying university filter:", self.university)
                conditions.append(
                    df["university"].str.contains(self.university, case=False, na=False)
                )
                filter_messages.append(f"university filter ({self.university})")

            # Filter by degree
            if self.degree:
                # print("Applying degree filter:", self.degree)
                conditions.append(
                    df["degree"].str.contains(self.degree, case=False, na=False)
                )
                filter_messages.append(f"degree filter ({self.degree})")

            # Filter by school
            if self.school:
                # print("Applying school filter:", self.school)
                conditions.append(
                    df["school"].str.contains(self.school, case=False, na=False)
                )
                filter_messages.append(f"school filter ({self.school})")

            # Handle year filtering but allow for future year if it's a prediction
            if self.year and not self.predict:
                conditions.append(
                    df["year"].str.contains(self.year, case=False, na=False)
                )
                filter_messages.append(f"year filter ({self.year})")
            elif self.predict:  # Allow predictions beyond the available years
                # Optionally, you could set a default filter range or adjust logic here
                conditions.append(
                    df["year"].astype(int) <= 2025
                )  # Use 2025 as upper limit for prediction

                # Combine all conditions with logical AND
            if conditions:
                df = df[np.logical_and.reduce(conditions)]

        # If the DataFrame is not empty, convert it to a dictionary
        filtered_data = df.to_dict(orient="records")

        return filtered_data


class Calculate:

    def __init__(self, extracted_keywords, data):
        self.input_keywords = extracted_keywords
        self.measure = extracted_keywords.get("measure", None)
        self.year = extracted_keywords.get("year", None)
        # self.mapped_columns = mapped_columns
        self.data = data

    def process(self):

        filter_entity = FilterEntity(
            self.data,
            self.input_keywords.get("degree"),
            self.input_keywords.get("university"),
            self.input_keywords.get("school"),
            self.input_keywords.get("year"),
        )
        filtered_data = filter_entity.apply_filters()
        df = pd.DataFrame(filtered_data)

        # print("Filtered data:", filtered_data)

        if len(filtered_data) == 0:
            result = "No relevant data found."
            return result

        # return filtered_data

        def process_result(result):
            result = {key: round(value) for key, value in result.items()}
            result_str = "\n ".join(
                [
                    f"{key.replace('_', ' ').title()}: S${value}"
                    for key, value in result.items()
                ]
            )
            return {"response": f"{result_str}"}

        try:

            # * Condition 1: If only salary is present in the measure [PASSED]
            # Calculate the mean of basic_monthly_mean, basic_monthly_median, gross_monthly_mean, gross_monthly_median based on the mapped columns
            if self.measure == ["salary"]:
                result = (
                    df[
                        [
                            "basic_monthly_mean",
                            "basic_monthly_median",
                            "gross_monthly_mean",
                            "gross_monthly_median",
                        ]
                    ]
                    .mean()
                    .to_dict()
                )
                return process_result(result)

            # * Condition 2: If salary and mean is present in the measure [PASSED]
            # Calculate the mean of basic_monthly_mean, gross_monthly_mean
            elif self.measure == ["salary", "mean"]:
                result = (
                    df[["basic_monthly_mean", "gross_monthly_mean"]].mean().to_dict()
                )
                return process_result(result)

            # * Condition 3: If salary and median is present in the measure [PASSED]
            # Calculate the mean of basic_monthly_median, gross_monthly_median
            elif self.measure == ["salary", "median"]:
                result = (
                    df[["basic_monthly_median", "gross_monthly_median"]]
                    .mean()
                    .to_dict()
                )
                return process_result(result)

            # * Condition 4: If salary, gross monthly is present in the measure [PASSED]
            # Calculate the mean of gross_monthly_mean, gross_monthly_median
            elif self.measure == ["salary", "gross"]:
                result = (
                    df[["gross_monthly_mean", "gross_monthly_median"]].mean().to_dict()
                )
                return process_result(result)

            # * Condition 5: If salary, gross monthly mean, is present in the measure [PASSED]
            # Calculate the mean of gross_monthly_mean
            elif self.measure == ["salary", "mean", "gross"]:
                result = df[["gross_monthly_mean"]].mean().to_dict()
                return process_result(result)

            # * Condition 6: If salary, gross monthly median is present in the measure [PASSED]
            # Calculate the mean of gross_monthly_median
            elif self.measure == ["salary", "median", "gross"]:
                result = df[["gross_monthly_median"]].mean().to_dict()
                return process_result(result)

        except Exception as e:
            return {"error": str(e)}


class Predict:
    def __init__(self, extracted_keywords, data):
        self.input_keywords = extracted_keywords
        self.measure = extracted_keywords.get("measure", None)
        self.year = extracted_keywords.get("year", None)
        self.data = data

    def linear_regression_predict(self, x, y, target_year):

        model = LinearRegression()
        model.fit(x, y)
        prediction = round(model.predict([[target_year]])[0])
        x_values = np.append(x, target_year)
        y_values = np.append(y, prediction)

        return (
            x_values.tolist(),
            y_values.tolist(),
            prediction,
        )

    def generate_chart(
        self, x_values, y_values, predicted_value, target_year, column_name
    ):
        import matplotlib

        matplotlib.use("Agg")

        plt.figure(figsize=(10, 6))
        plt.scatter(x_values, y_values, color="blue", label="Historical Data")
        plt.plot(x_values, y_values, color="blue", linestyle="--", label="Trend Line")
        plt.scatter(target_year, predicted_value, color="red", label="Predicted Value")
        plt.title(
            f'{column_name.replace("_", " ").title()} Prediction for {target_year}'
        )
        plt.xlabel("Year")
        plt.ylabel(column_name.replace("_", " ").title())
        plt.legend()
        plt.grid(True)

        # Save the chart to a BytesIO object
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format="png")
        plt.close()
        img_buffer.seek(0)

        # Encode the BytesIO object as a base64 string
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode("utf-8")
        return img_base64

    def process(self):
        # Step 1: Filter the data based on the provided keywords
        filter_entity = FilterEntity(
            self.data,
            self.input_keywords.get("degree"),
            self.input_keywords.get("university"),
            self.input_keywords.get("school"),
            self.input_keywords.get("year"),
            predict=True,
        )
        filtered_data = filter_entity.apply_filters()
        df = pd.DataFrame(filtered_data)

        # print("Filtered data columns:", df.columns)

        if len(filtered_data) == 0:
            return "No relevant data found."

        # Step 2: Determine the target year for prediction
        try:
            # Use the user-provided year if it is valid
            if self.year and isinstance(self.year, (int, str)):
                target_year = int(self.year)
            else:
                # Fall back to the next year if no valid year is provided
                x = np.array(df["year"].astype(int)).reshape(-1, 1)  # Features (year)
                target_year = max(x)[0] + 1  # Predict the next year

            # Step 3: Validate the target year
            min_year = min(df["year"].astype(int))
            max_year = max(df["year"].astype(int))

            # If the target year is within the dataset range, use Calculate instead of Predict
            if min_year <= target_year <= max_year:

                # Fall back to the Calculate class to get the actual data
                calculate = Calculate(self.input_keywords, self.data)

                result = calculate.process()["response"]
                # If the result is a string, split it into lines (if needed)
                if isinstance(result, str):
                    result = result.split("\n")

                result_str = "\n".join(
                    [f"- {item.strip()}" for item in result if item.strip()]
                )

                return {
                    "response": f"The result for {target_year} is not a prediction but exists in the current dataset. \nHere are the actual values: \n{result_str} \n<em>For prediction input a year after 2022<em>"
                }

            # Step 4: Process self.measure
            x = np.array(df["year"].astype(int)).reshape(-1, 1)  # Features (year)

            predictions = {}

            # * Condition 1: If only salary is present in the measure
            if self.measure == ["salary"]:
                columns = [
                    "basic_monthly_mean",
                    "basic_monthly_median",
                    "gross_monthly_mean",
                    "gross_monthly_median",
                ]
                for col in columns:
                    if col in df.columns:
                        x_values, y_values, prediction = self.linear_regression_predict(
                            x, np.array(df[col].astype(float)), target_year
                        )
                        chart_buffer = self.generate_chart(
                            x_values, y_values, prediction, target_year, col
                        )
                        predictions[col] = {
                            "x": x_values,
                            "y": y_values,
                            "predicted_value": prediction,
                            "chart": chart_buffer,
                        }

            # * Condition 2: If salary and mean is present in the measure
            elif self.measure == ["salary", "mean"]:
                columns = ["basic_monthly_mean", "gross_monthly_mean"]
                for col in columns:
                    if col in df.columns:
                        x_values, y_values, prediction = self.linear_regression_predict(
                            x, np.array(df[col].astype(float)), target_year
                        )
                        chart_buffer = self.generate_chart(
                            x_values, y_values, prediction, target_year, col
                        )
                        predictions[col] = {
                            "x": x_values,
                            "y": y_values,
                            "predicted_value": prediction,
                            "chart": chart_buffer,
                        }

            # * Condition 3: If salary and median is present in the measure
            elif self.measure == ["salary", "median"]:
                columns = ["basic_monthly_median", "gross_monthly_median"]
                for col in columns:
                    if col in df.columns:
                        x_values, y_values, prediction = self.linear_regression_predict(
                            x, np.array(df[col].astype(float)), target_year
                        )
                        predictions[col] = {
                            "x": x_values,
                            "y": y_values,
                            "predicted_value": prediction,
                        }

            # * Condition 4: If salary, gross monthly is present in the measure
            elif self.measure == ["salary", "gross"]:
                columns = ["gross_monthly_mean", "gross_monthly_median"]
                for col in columns:
                    if col in df.columns:
                        x_values, y_values, prediction = self.linear_regression_predict(
                            x, np.array(df[col].astype(float)), target_year
                        )
                        predictions[col] = {
                            "x": x_values,
                            "y": y_values,
                            "predicted_value": prediction,
                        }

            # * Condition 5: If salary, gross monthly mean, is present in the measure
            elif self.measure == ["salary", "mean", "gross"]:
                columns = ["gross_monthly_mean"]
                for col in columns:
                    if col in df.columns:
                        x_values, y_values, prediction = self.linear_regression_predict(
                            x, np.array(df[col].astype(float)), target_year
                        )
                        predictions[col] = {
                            "x": x_values,
                            "y": y_values,
                            "predicted_value": prediction,
                        }

            # * Condition 6: If salary, gross monthly median is present in the measure
            elif self.measure == ["salary", "median", "gross"]:
                columns = ["gross_monthly_median"]
                for col in columns:
                    if col in df.columns:
                        x_values, y_values, prediction = self.linear_regression_predict(
                            x, np.array(df[col].astype(float)), target_year
                        )
                        chart_buffer = self.generate_chart(
                            x_values, y_values, prediction, target_year, col
                        )
                        predictions[col] = {
                            "x": x_values,
                            "y": y_values,
                            "predicted_value": prediction,
                            "chart": chart_buffer,
                        }

            else:
                return f"Measure '{self.measure}' is not supported for prediction."

            if not predictions:
                return f"No valid columns found for measure '{self.measure}'."

            result_str = f"For {target_year}, the predicted {self.measure[0]} is:\n"
            result_str += "\n".join(
                [
                    f"{col.replace('_', ' ').title()}: S${data['predicted_value']}"
                    for col, data in predictions.items()
                ]
            )

            return {
                "predicted_value": [
                    data["predicted_value"] for data in predictions.values()
                ],
                "charts": [
                    data["chart"] for data in predictions.values()
                ],  # Include chart buffers
                "response": result_str,
            }

        except Exception as e:
            return {"response": f"Error during prediction: {str(e)}"}


class Compare:

    def __init__(self, extracted_keywords):
        self.user_input = extracted_keywords
        pass

    def process(self):
        print("Processing Compare")
        pass

    pass


class Analyze:

    def __init__(self, extracted_keywords):
        self.user_input = extracted_keywords
        pass

    def process(self):
        print("Processing Analyze")
        pass

    pass
