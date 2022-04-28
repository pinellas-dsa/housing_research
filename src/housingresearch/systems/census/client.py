from typing import List
from census_area import Census
from us import states

from housingresearch.config import settings

Records = List[dict]


class CensusClient:
    """Handles interaction with the census API"""

    def __init__(self) -> None:
        self.census = self.connect()
        self.queries = []

    @property
    def is_connected(self) -> bool:
        """Returns True if connection to census is successful"""
        return self.census.session.verify

    def connect(self) -> Census:
        """Creates a connection to the Census by providing API key"""
        return Census(settings.census_api_key)

    def run_queries(self, specs: Records):
        """Loops through records and runs a Query for each set of specifications."""
        for spec in specs:
            query = Query(spec, self.census)
            self.queries.append(query)


class Query:
    """Stores all the information about a query, including its census
    type, its year, the table name, and the results."""

    def __init__(
        self,
        spec: dict,
        conn: Census,
    ) -> None:
        """Defines the basics parameters for a query"""
        try:
            self.table_name = spec["table_name"]
            self.survey = spec["survey"]
            self.year = spec["year"]
            self.state = spec["state"]
            self.place = spec["place"]
            self.level = spec["level"]
        except KeyError as err:
            raise err
        self.conn = conn
        self.variables = ()

    def get_table_variables(self, table_name: str, lookup: dict) -> None:
        """Given a table name and a lookup dict, returns a tuple
        with the names of every variable and error term for that
        table.
        """
        if table_name in lookup:
            print(f"Found lookup data for table {table_name}.")
            table_specs = lookup.get(table_name)
            metrics = [
                table_name + "_" + var + "E"
                for var in table_specs["variables"]
            ]
            errors = [
                table_name + "_" + var + "M"
                for var in table_specs["variables"]
            ]
            variables = tuple(metrics + errors)
        else:
            raise KeyError("Table not found in lookup.")
        self.variables = variables

    def get_data_by_tract(self):
        """When we want the data grouped by tract, this method
        pings the census API and gets it in that form."""
        api_results = self.conn.census.acs5.state_place_tract(
            fields=self.variables,
            state=states.FL.fips,
            place=63000,
            year=2019,
            return_geometry=False,
        )
        return api_results
