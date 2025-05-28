# config\prompt_structure.py

from app.routes.data_gov_api import fetch_data
import pandas as pd


categories = {
    "entity": {
        "university": [
            {
                "synonym_universities": {
                    "Nanyang Technological University": [
                        "NTU",
                        "Nanyang Technological",
                    ],
                    "National University of Singapore": [
                        "NUS",
                        "National University Singapore",
                    ],
                    "Singapore Management University": [
                        "SMU",
                    ],
                    "Singapore Institute of Technology": [
                        "SIT",
                    ],
                    "Singapore University of Technology and Design": [
                        "SUTD",
                    ],
                    "Singapore University of Social Sciences": [
                        "SUSS",
                    ],
                }
            }
        ],
        "school": [],  # stored by add_unique_values_column, called in user.py
        "degree": [],  # stored by add_unique_values_column, called in user.py
    },
    "operation": [
        {
            "synonym_operations": {
                "extract": [
                    "extract data",
                    "pull data",
                    "retrieve data",
                ],
                "calculate": [
                    "compute",
                    "determine",
                    "figure out",
                    "find",
                    "show",
                    "what",
                ],
                "predict": [
                    "forecast",
                    "estimate",
                    "project",
                ],
                "compare": ["contrast", "evaluate", "analyze differences", "vs"],
                "analyze": ["examine", "study", "scrutinize", "analyse"],
            }
        }
    ],
    "time": ["2025", "year", "quarter", "month", "time"],
}


def add_unique_values_column(data):
    # * Extract data from public api
    df = data
    df = pd.DataFrame(df)
    df = df.dropna()

    # * Extract unique school from dataset
    unique_schools = df["school"].dropna().unique()
    unique_schools_list = unique_schools.tolist()
    categories["entity"]["school"] = unique_schools_list

    # * Extract unique degree from dataset
    unique_degree = df["degree"].dropna().unique()
    unique_degree_list = unique_degree.tolist()
    categories["entity"]["degree"] = unique_degree_list

    return unique_schools_list, unique_degree_list


synonym_universities = {
    "NTU": "Nanyang Technological University",
    "NUS": "National University of Singapore",
    "SIT": "Singapore Institute of Technology",
    "SMU": "Singapore Management University",
    "SUTD": "Singapore University of Technology and Design",
    "SUSS": "Singapore University of Social Sciences",
}

synonym_measures = {
    "salary": ["income", "wage", "pay", "wages", "incomes", "pays"],
    "rate": ["percentage", "rate of return"],
    "median": ["middle value", "midpoint"],
    "mean": ["average"],
    "gross": ["before deductions", "before tax", "gross monthly"],
    "employment rate": ["job rate", "employment percentage"],
    "percentile": ["percent", "ranking"],
}

query_types = [
    {"type": "Lookup", "keywords": ["what", "which", "where", "retrieve", "find"]},
    {
        "type": "Comparison",
        "keywords": [
            "compare",
            "difference",
            "vs",
            "greater",
            "less",
            "highest",
            "lowest",
            "most",
        ],
    },
    {
        "type": "Aggregation",
        "keywords": [
            "average",
            "mean",
            "sum",
            "total",
            "median",
            "largest",
            "greatest",
            "smallest",
        ],
    },
    {"type": "Prediction", "keywords": ["predict", "forecast", "estimate"]},
    {"type": "Analysis", "keywords": ["analyze", "trend", "pattern", "insight"]},
]

column_mapping = {
    "salary": {
        "mean": "basic_monthly_mean",
        "median": "basic_monthly_median",
        "gross": "gross_monthly_mean",
        "gross_median": "gross_monthly_median",
    },
    "employment_rate": {
        "overall": "employment_rate_overall",
        "full_time_permanent": "employment_rate_ft_perm",
    },
    "year": "year",
}
