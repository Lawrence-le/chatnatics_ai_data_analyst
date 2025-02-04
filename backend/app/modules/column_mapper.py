# app\modules\column_mapper.py


class ColumnMapper:
    def __init__(self, column_mapping):
        self.column_mapping = column_mapping

    def map_to_column(self, extracted_keywords):
        """
        Map the extracted keywords to the relevant column names.
        """
        mapped_columns = []

        # # 1. Handle 'measure' mapping
        # if "measure" in extracted_keywords:
        #     measure_keywords = extracted_keywords["measure"]
        #     for keyword in measure_keywords:
        #         for key, values in self.column_mapping.items():
        #             if isinstance(values, dict):
        #                 for sub_key, column in values.items():
        #                     if sub_key.lower() in keyword.lower():
        #                         mapped_columns.append(column)
        #             elif keyword.lower() in values.lower():
        #                 mapped_columns.append(values)

        # 2. Handle 'degree' mapping (directly map to the degree column)
        if "degree" in extracted_keywords:
            degree = extracted_keywords["degree"]
            # 'degree' is a column in the dataset, so map directly to it
            mapped_columns.append("degree")

        # 3. Handle 'university' mapping (directly map to the university column)
        if "university" in extracted_keywords:
            university = extracted_keywords["university"]
            # 'university' is a column in the dataset, so map directly to it
            mapped_columns.append("university")

        # 4. Handle 'year' mapping (this comes from the column_mapping itself)
        if "time_period" in extracted_keywords:
            time_period = extracted_keywords["time_period"]
            mapped_columns.append("year")

        return mapped_columns
