import pytest

from housingresearch.config import settings
from housingresearch.systems import CensusClient

# collect_ignore = ["integration_tests"]

GOOD_SPECS = [
    {
        "table_name": "B25070",
        "survey": "acs5",
        "year": 2019,
        "state": "FL",
        "place": "63000",
        "level": "tract",
    },
    {
        "table_name": "B25034",
        "survey": "acs5",
        "year": 2019,
        "state": "FL",
        "place": "63000",
        "level": "tract",
    },
]
BAD_SPECS = [
    {"table_name": "a", "survey_year": "b"},
    {"table_name": "a", "survey_year": "b"},
]


@pytest.fixture(scope="session")
def test_config():
    """Returns the configuration settings for use in tests"""
    test_settings = settings.from_env("testing")
    return test_settings


@pytest.fixture(scope="session", name="test_census")
def fixture_test_census():
    """Creates an authenticated Census client for use in integration tests"""
    return CensusClient()


@pytest.fixture(scope="session", name="test_query")
def fixture_test_query():
    """Runs a query from an authenticated Census client for use in integration tests"""
    specs = GOOD_SPECS
    census = CensusClient()
    census.run_queries(specs)
    return census.queries[0]


@pytest.fixture(scope="session", name="test_bad_query")
def fixture_test_bad_query():
    """Runs a query from an authenticated Census client for use in integration tests"""
    specs = BAD_SPECS
    census = CensusClient()
    census.run_queries(specs)
