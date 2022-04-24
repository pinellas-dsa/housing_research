from housingresearch.systems import CensusClient


class TestCensusClient:
    """Tests for the Person class"""

    def test_init(self):
        """Tests __init__() for Census and validates that:
        - Object initializes.
        """
        # execution
        census = CensusClient()
        # validation
        assert isinstance(census, CensusClient)

    def test_connection(self):
        """Tests that new CensusClient object correctly successfully to the API."""
        # execution
        census = CensusClient()
        # validation
        assert census.is_connected
