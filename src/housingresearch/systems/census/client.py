from typing import List, Tuple
import pandas as pd
from census_area import Census
from us import states
from loguru import logger
from tenacity import retry, stop_after_attempt
from housingresearch.config import settings
from housingresearch.systems.census import ACS5_TABLES

Records = List[dict]


class CensusClient:
    """Handles interaction with the census API"""

    def __init__(self) -> None:
        self.census: Census = self.connect()
        self.queries: List = []

    @property
    def is_connected(self) -> bool:
        """Returns True if connection to census is successful"""
        return self.census.session.verify

    def connect(self) -> Census:
        """Creates a connection to the Census by providing API key"""
        return Census(settings.census_api_key)

    def run_queries(self, specs: Records, table_lookup: dict = None):
        """Loops through records and runs a Query for each set of specifications."""
        for spec in specs:
            if spec["survey"] == "acs5":
                table_lookup = ACS5_TABLES
            query = Query(spec, self.census, table_lookup)
            self.queries.append(query)


class Query:
    """Stores all the information about a query, including its census
    type, its year, the table name, and the results."""

    # pylint: disable=broad-except
    # Seems weird to import an EsriError class that contains only "pass"

    def __init__(
        self, spec: dict, conn: Census, table_lookup: dict = None
    ) -> None:
        """Defines the basics parameters for a query"""
        self.spec = spec
        if self.spec["table_name"] in table_lookup:
            print(f"Found lookup data for table {self.spec['table_name']}.")
            self.lookup: dict = table_lookup.get(self.spec["table_name"])
        else:
            raise KeyError("Table not found in lookup.")
        self.conn: Census = conn
        self.variables: Tuple[str] = self.get_table_variables(
            self.spec["table_name"]
        )
        if self.spec["level"] == "tract":
            self.api_results: Records = self.get_data_by_tract()
            logger.info("Query instantiated.")
        if self.api_results:
            self.dataframe = self.to_dataframe()

    def get_table_variables(self, table_name: str) -> Tuple[str]:
        """Given a table name, returns a tuple with the names of every
        variable and error term for that table.
        """
        metrics = [
            table_name + "_" + var + "E" for var in self.lookup["variables"]
        ]
        errors = [
            table_name + "_" + var + "M" for var in self.lookup["variables"]
        ]
        variables = tuple(metrics + errors)
        return variables

    @retry(stop=stop_after_attempt(7))
    def get_data_by_tract(self) -> Tuple[str]:
        """When we want the data grouped by tract, this method
        pings the census API and gets it in that form.
        """
        if self.spec["survey"] == "acs5":
            client = self.conn.acs5
        elif self.spec["survey"] == "sf1":
            client = self.conn.sf1
        try:
            logger.info("Querying Census API.")
            api_results = client.state_place_tract(
                fields=self.variables,
                state=states.FL.fips,
                place=self.spec["place"],
                year=self.spec["year"],
                return_geometry=False,
            )
            logger.info("Query successful!")
        except Exception as err:
            raise f"{type(err).__name__} was raised."
        return api_results

    def to_dataframe(self) -> pd.DataFrame:
        """Converts the records stored in self.api_results to a DataFrame
        format. The DataFrame is originally in "wide" format with all variables
        in their own column, but we then convert to "long" format with one row
        per observation.
        """
        df_wide = pd.DataFrame.from_records(self.api_results)
        df_wide["year"] = self.spec["year"]
        df_wide["place"] = self.spec["place"]
        df_wide["table"] = self.spec["table_name"]
        df_wide.columns = [
            col.replace(self.spec["table_name"] + "_", "")
            for col in df_wide.columns
        ]
        df_long = pd.melt(
            df_wide,
            id_vars=["table", "state", "county", "tract", "year"],
            value_vars=[
                colname
                for colname in df_wide.columns
                if colname.endswith("E") or colname.endswith("M")
            ],
        )
        df_long["suffix"] = df_long["variable"].str[-1]
        df_long["variable"] = df_long["variable"].str[:-1]
        df_long = self.add_variable_name_column(df_long)
        return df_long

    def add_variable_name_column(
        self, dataframe: pd.DataFrame
    ) -> pd.DataFrame:
        """Uses the Query.lookup dictionary to identify the name of each variable
        in the self.dataframe attribute. Writes these names to a new column in the dataframe.
        """
        dataframe["variable_name"] = dataframe.apply(
            lambda x: self.lookup["variables"].get(x.variable).get("label"),
            axis=1,
        )
        return dataframe

    # class Spec:
    #     def __init__(
    #         self,
    #         table_name: str,
    #         survey: str,
    #         year: int,
    #         state: str,
    #         place: str,
    #         level: str,
    #     ) -> None:
    #         """"""
    #         self.table_name = table_name
    #         self.survey = survey
    #         self.year = year
    #         self.state = state
    #         self.place = place
    #         self.level = level
