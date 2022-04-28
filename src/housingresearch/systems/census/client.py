from census_area import Census
from typing import List, Tuple
from us import states


from housingresearch.config import settings

Records = List[dict]


class CensusClient:
    """Handles interaction with the census API"""

    def __init__(self, queries: tuple) -> None:
        self.census = self.connect()
        for query in queries:
            pass

    @property
    def is_connected(self) -> bool:
        """Returns True if connection to census is successful"""
        return self.census.session.verify

    def connect(self) -> Census:
        """Creates a connection to the Census by providing API key"""
        return Census(settings.census_api_key)


class Query:
    """Stores all the information about a query, including its census
    type, its year, the table name, and the results."""

    def __init__(
        self,
        table_name: str,
        survey: str,
        year: int,
        connection: Census,
        state: str = "FL",
        place: str = "63000",
        level: str = "tract",
    ) -> None:
        """Defines the basics parameters for a query"""
        self.table_name = table_name
        self.survey = survey
        self.year = year
        self.connection = connection
        self.state = state
        self.place = place
        self.level = level

    def get_table_vars(self, table_name: str, lookup: dict) -> Tuple[str]:
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
            vars = tuple(metrics + errors)
        else:
            raise "Table not found in lookup."
        self.vars = vars

    def get_data_by_tract(self):
        api_results = self.connection.census.acs5.state_place_tract(
            fields=self.vars,
            state=states.FL.fips,
            place=63000,
            year=2019,
            return_geometry=False,
        )