from typing import List, Tuple
from census_area import Census
from us import states
from loguru import logger
from tenacity import retry, stop_after_attempt
from housingresearch.config import settings
from housingresearch.systems.census import ACS_TABLES

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
                table_lookup = ACS_TABLES
            query = Query(spec, self.census, table_lookup)
            self.queries.append(query)


class Query:
    """Stores all the information about a query, including its census
    type, its year, the table name, and the results."""

    # pylint: disable=too-many-instance-attributes
    # Ten attributes is reasonable in this case.
    # pylint: disable=broad-except
    # Seems weird to import an EsriError class that contains only "pass"

    # TODO: create a "Spec" class
    # TODO: store the spec together with the Query so that we can lookup its year etc

    def __init__(
        self, spec: dict, conn: Census, table_lookup: dict = None
    ) -> None:
        """Defines the basics parameters for a query"""
        try:
            self.table_name = spec["table_name"]
            self.survey: str = spec["survey"]
            self.year: int = spec["year"]
            self.state: str = spec["state"]
            self.place: str = spec["place"]
            self.level: str = spec["level"]
        except KeyError as err:
            raise err
        self.table_lookup: dict = table_lookup
        self.conn: Census = conn
        self.variables: Tuple[str] = self.get_table_variables(
            self.table_name, self.table_lookup
        )
        if self.level == "tract":
            try:
                self.api_results: Records = self.get_data_by_tract()
            except Exception:
                logger.info("API Query Failed")
        logger.info("Query instantiated.")

    def get_table_variables(self, table_name: str, lookup: dict) -> Tuple[str]:
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
        return variables

    @retry(stop=stop_after_attempt(7))
    def get_data_by_tract(self) -> Tuple[str]:
        """When we want the data grouped by tract, this method
        pings the census API and gets it in that form.
        """
        if self.survey == "acs5":
            client = self.conn.acs5
        elif self.survey == "sf1":
            client = self.conn.sf1
        try:
            logger.info("Querying Census API.")
            api_results = client.state_place_tract(
                fields=self.variables,
                state=states.FL.fips,
                place=self.place,
                year=self.year,
                return_geometry=False,
            )
            logger.info("Query successful!")
        except Exception as err:
            print(f"{type(err).__name__} was raised.")
        return api_results
