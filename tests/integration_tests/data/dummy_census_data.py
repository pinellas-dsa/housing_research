import pandas as pd

MOCK_TABLES = {
    "B25070": {  # lookup code for one table
        "table_name": "This is the table's whole long name in English",
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
    "B25070_001E",
    "B25070_002E",
    "B25070_003E",
    "B25070_004E",
    "B25070_005E",
    "B25070_006E",
    "B25070_007E",
    "B25070_008E",
    "B25070_009E",
    "B25070_010E",
    "B25070_011E",
    "B25070_001M",
    "B25070_002M",
    "B25070_003M",
    "B25070_004M",
    "B25070_005M",
    "B25070_006M",
    "B25070_007M",
    "B25070_008M",
    "B25070_009M",
    "B25070_010M",
    "B25070_011M",
)

GOOD_SPECS = [
    {
        "table_name": "B25070",
        "survey": "acs5",
        "year": 2019,
        "state": "FL",
        "place": "09625",
        "level": "tract",
    },
    {
        "table_name": "B25070",
        "survey": "acs5",
        "year": 2012,
        "state": "FL",
        "place": "09625",
        "level": "tract",
    },
]
BAD_SPECS = [
    {"table_name": "B1", "survey_year": 3},
    {"table_name": "B2", "survey_year": 4},
]

EXPECTED_COLS = [
    "table",
    "state",
    "county",
    "tract",
    "year",
    "variable",
    "variable_name",
    "value",
    "suffix",
]
