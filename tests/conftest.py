import pytest
from housingresearch.config import settings
from housingresearch.systems import CensusClient
from tests.integration_tests.data.dummy_census_data import (
    MOCK_TABLES,
    GOOD_SPECS,
)

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


@pytest.fixture(scope="session", name="test_query_dataframe")
def fixture_test_query_dataframe():
    """Creates the DataFrame attribute on an object of class Query
    for use in integration tests
    """
    test_census = CensusClient()
    test_census.run_queries(GOOD_SPECS, MOCK_TABLES)
    query = test_census.queries[0]
    return query.dataframe
