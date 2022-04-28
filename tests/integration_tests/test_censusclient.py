import pytest
from housingresearch.systems import CensusClient, Query
from tests.conftest import BAD_SPECS


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


class TestQuery:
    """Tests for the Query class"""

    def test_init(self, test_query):
        """Tests that the new Query object initializes successfully and has type Query."""
        # validation
        assert isinstance(test_query, Query)

    def test_bad_spec_fails(self):
        """"""
        # setup
        specs = BAD_SPECS
        census = CensusClient()
        # validation
        with pytest.raises(KeyError):

            census.run_queries(specs)
