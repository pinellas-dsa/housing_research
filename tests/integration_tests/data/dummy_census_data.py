import pandas as pd

MOCK_TABLES = {
    "B1": {  # lookup code for one table
        "table_name": "B1",
        "variables": {
            "001": {
                "label": "0 to 1",
                "value": pd.NA,
                "error": pd.NA,
            },
            "002": {
                "label": "Less than 1",
                "value": pd.NA,
                "error": pd.NA,
            },
            "003": {
                "label": "1 to 2",
                "value": pd.NA,
                "error": pd.NA,
            },
            "004": {
                "label": "2 to 3",
                "value": pd.NA,
                "error": pd.NA,
            },
            "005": {
                "label": "3 to 4",
                "value": pd.NA,
                "error": pd.NA,
            },
        },
    },
}


MOCK_VARIABLES = (
    "B1_001E",
    "B1_002E",
    "B1_003E",
    "B1_004E",
    "B1_005E",
    "B1_001M",
    "B1_002M",
    "B1_003M",
    "B1_004M",
    "B1_005M",
)

GOOD_SPECS = [
    {
        "table_name": "B1",
        "survey": "mock_survey",
        "year": 2019,
        "state": "FL",
        "place": "63000",
        "level": "tract",
    },
    {
        "table_name": "B1",
        "survey": "mock_survey",
        "year": 2020,
        "state": "FL",
        "place": "63000",
        "level": "tract",
    },
]
BAD_SPECS = [
    {"table_name": "B1", "survey_year": 3},
    {"table_name": "B2", "survey_year": 4},
]
