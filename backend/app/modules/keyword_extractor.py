# app\modules\KeywordExtractor.py
import re

# from config.prompt_structure import extracted_keywords, categories


class KeywordExtractor:

    def __init__(self, categories, synonym_measures):
        self.categories = categories
        self.synonym_measures = synonym_measures

    def extract_keywords(self, user_input):

        # Initialize/reset extracted_keywords for every request
        self.extracted_keywords = {
            "university": None,
            "degree": None,
            "school": None,
            "measure": None,
            "operation": None,
            "year": [],
        }

        # Extract keywords for each category (entities, measures, operations, etc.)
        self.extract_entities(user_input)
        self.extract_measures(user_input)
        self.extract_operations(user_input)
        self.extract_year(user_input)

        return self.extracted_keywords

    def re_search_compiler(self, user_input, key, value):
        """
        Search for a value in the user input and add it to the extracted_keywords dictionary.
        """
        if re.search(r"\b" + re.escape(value) + r"\b", user_input, re.IGNORECASE):
            self.extracted_keywords[key] = value

    def extract_entities(self, user_input):
        """
        Extract entity-related keywords from the user input (e.g., school, course, university).
        """
        for university_dict in self.categories["entity"]["university"]:
            for full_name, synonyms in university_dict["synonym_universities"].items():
                # Check if the full name appears in the user input
                self.re_search_compiler(user_input, "university", full_name)

                # Check if any synonym appears in the user input
                if isinstance(synonyms, list):  # If synonyms are in a list
                    for synonym in synonyms:
                        # If a synonym is found, store the full name (not the synonym) in the extracted keywords
                        if re.search(
                            r"\b" + re.escape(synonym) + r"\b",
                            user_input,
                            re.IGNORECASE,
                        ):
                            self.extracted_keywords["university"] = full_name

        for value in self.categories["entity"]["school"]:
            self.re_search_compiler(user_input, "school", value)

        for value in self.categories["entity"]["degree"]:
            self.re_search_compiler(user_input, "degree", value)

    def extract_measures(self, user_input):
        """
        Extract measure-related keywords from the user input (e.g., salary, median).
        This function should also be able to handle multiple related keywords for mapping.
        """
        # Track which keywords were found in the input
        matched_keywords = []

        # Iterate over the list of measure-related keywords
        for measure, synonyms in self.synonym_measures.items():
            # Check for the measure keyword or any of its synonyms in the user input
            all_keywords = [
                measure
            ] + synonyms  # include both the main measure and synonyms
            for value in all_keywords:
                if re.search(
                    r"\b" + re.escape(value) + r"\b", user_input, re.IGNORECASE
                ):
                    if measure not in matched_keywords:  # Only add once
                        matched_keywords.append(
                            measure
                        )  # Use the main measure name (e.g., "salary")

        # If any keywords were matched, add them to the extracted_keywords dictionary
        if matched_keywords:
            self.extracted_keywords["measure"] = matched_keywords

    # def extract_operations(self, user_input):
    #     """
    #     Extract operation-related keywords from the user input (e.g., calculate, analyze).
    #     """
    #     for value in self.categories["operation"]:
    #         self.re_search_compiler(user_input, "operation", value)
    #         if self.extracted_keywords.get("operation"):
    #             break

    def extract_operations(self, user_input):
        """
        Extract operation-related keywords from the user input (e.g., calculate, analyze).
        """
        # Iterate over the operations in the categories and check for synonyms
        for operation_dict in self.categories["operation"]:
            for operation, synonyms in operation_dict.get("synonym_operations").items():
                self.re_search_compiler(user_input, "operation", operation)
                # Check if the operation or any of its synonyms appear in the user input
                if isinstance(synonyms, list):  # If synonyms are in a list
                    for synonym in synonyms:
                        if re.search(
                            r"\b" + re.escape(synonym) + r"\b",
                            user_input,
                            re.IGNORECASE,
                        ):
                            self.extracted_keywords["operation"] = operation

    def extract_year(self, user_input):
        """
        Extract time-related keywords from the user input (e.g., year, month, 2025).
        """
        # First, check for a year (e.g., 2026, 1998)
        year_match = re.search(r"\b20\d{2}\b", user_input)
        if year_match:
            self.extracted_keywords["year"] = year_match.group(0)
            return  # Exit after finding the year

        # # If no year is found, check for predefined time keywords (like '2025', 'January', etc.)
        # for value in self.categories["time"]:
        #     self.re_search_compiler(user_input, "time", value)
        #     if self.extracted_keywords.get("time"):
        #         break
