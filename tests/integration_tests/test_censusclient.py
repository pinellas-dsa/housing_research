from housingresearch.systems import CensusClient, Query


class TestCensusClient:
    """Tests for the CensusClient class"""

    def test_init(self, test_census):
        """Tests __init__() for Census and validates that:
        - Object initializes.
        """
        # validation
        assert isinstance(test_census, CensusClient)

    def test_connection(self, test_census):
        """Tests that new CensusClient object correctly successfully to the API."""
        # validation
        assert test_census.is_connected


class TestQuery:
    """Tests for the Query class"""

    def test_init(self, test_query):
        """"""
        # validation
        assert isinstance(test_query, Query)
