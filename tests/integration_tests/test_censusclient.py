import pandas as pd
import pytest
from housingresearch.systems import CensusClient, Query
from tests.integration_tests.data.dummy_census_data import (
    EXPECTED_COLS,
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
        query.get_table_variables(table_name=query.spec["table_name"])
        # validation
        assert query.variables == expected

    def test_query_to_dataframe_returns_df(self, test_census):
        """Tests that the `to_dataframe()` method of the Query class
        produces an object of class DataFrame.
        """
        # execution
        test_census.run_queries(GOOD_SPECS, MOCK_TABLES)
        query = test_census.queries[0]
        dataframe = query.to_dataframe()
        assert isinstance(dataframe, pd.DataFrame)

    def test_query_to_dataframe_returns_expected_cols(
        self, test_query_dataframe
    ):
        """Tests that the dataframe attribute on an object of
        class Query has the expected columns.
        """
        # setup
        expected_cols = EXPECTED_COLS
        # validation
        dataframe = test_query_dataframe
        assert sorted(dataframe.columns) == sorted(expected_cols)

    def test_dataframe_variables_are_numeric(self, test_query_dataframe):
        """Tests that values in the column 'variable' are all
        numeric strings.
        """
        # setup
        dataframe = test_query_dataframe
        assert all(dataframe["variable"].str.isnumeric())

    def test_dataframe_variable_names_are_correct(self, test_query_dataframe):
        """Tests that the column 'variable_name' has the correct names for
        known variables.
        """
        # setup
        dataframe = test_query_dataframe
        cond_001 = dataframe["variable"] == "001"
        cond_002 = dataframe["variable"] == "002"
        cond_003 = dataframe["variable"] == "003"
        # validation
        assert dataframe[cond_001]["variable_name"].iloc[0] == "Total"
        assert (
            dataframe[cond_002]["variable_name"].iloc[0]
            == "Less than 10.0 Percent"
        )
        assert (
            dataframe[cond_003]["variable_name"].iloc[0]
            == "10.0 to 14.9 Percent"
        )
