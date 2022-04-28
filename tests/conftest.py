from pathlib import Path
import pytest

from housingresearch.config import settings
from housingresearch.systems import CensusClient, Query

# collect_ignore = ["integration_tests"]


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
    specs = [
        {"table_name": "a", "survey_year": "b"},
        {"table_name": "a", "survey_year": "b"},
    ]
    census = CensusClient()
    census.run_queries(specs)
    return census.queries[0]