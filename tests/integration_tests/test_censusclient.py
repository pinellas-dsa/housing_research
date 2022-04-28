import pytest
from housingresearch.systems import CensusClient, Query
from tests.integration_tests.data import (
    MOCK_TABLES,
    MOCK_VARIABLES,
    GOOD_SPECS,
    BAD_SPECS,
)


class TestCensusClient:
    """Tests for the CensusClient class"""

    def test_init(self, test_census):
        """Tests __init__() for Census and validates that:
        - Object initializes.
        """
        # validation
        assert isinstance(test_census, CensusClient)

    def test_connection(self, test_census):
        """Tests that new CensusClient object connects correctly successfully to the API."""
        # validation
        assert test_census.is_connected

    def test_run_queries_fails_given_bad_specs(self, test_census):
        """Tests that a call to CensusClient.run_queries fails with a
        KeyError if specs are poorly formed.
        """
        # setup
        specs = BAD_SPECS
        # validation
        with pytest.raises(KeyError):
            test_census.run_queries(specs)


class TestQuery:
    """Tests for the Query class"""

    def test_init(self, test_census):
        """Tests that the new Query object initializes successfully and has type Query."""
        # execution
        test_census.run_queries(GOOD_SPECS, MOCK_TABLES)
        query = test_census.queries[0]
        # validation
        assert isinstance(query, Query)

    def test_get_table_variables(self, test_census):
        """Tests that the method Query.get_table_variables() produces the expected
        tuple of results.
        """
        # setup
        expected = MOCK_VARIABLES
        # execution
        test_census.run_queries(GOOD_SPECS, MOCK_TABLES)
        query = test_census.queries[0]
        query.get_table_variables(table_name="B1", lookup=MOCK_TABLES)
        # validation
        assert query.variables == expected

    def test_get_table_variables_fails_when_table_name_not_in_lookup(
        self, test_census
    ):
        """Tests that a KeyError is raised when given a table name that
        isn't listed in the lookup.
        """
        # execution
        test_census.run_queries(GOOD_SPECS, MOCK_TABLES)
        query = test_census.queries[0]
        # validation
        with pytest.raises(KeyError):
            query.get_table_variables(table_name="B3", lookup=MOCK_TABLES)
