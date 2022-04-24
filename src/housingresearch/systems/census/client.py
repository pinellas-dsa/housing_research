from census import Census

# from us import states

from housingresearch.config import settings


class CensusClient:
    """Handles interaction with the census API"""

    def __init__(self) -> None:
        self.census = self.connect()

    @property
    def is_connected(self) -> bool:
        """Returns True if connection to census is successful"""
        return self.census.session.verify

    def connect(self) -> Census:
        """Creates a connection to the Census by providing API key"""
        return Census(settings.census_api_key)

    # def

    # get = census.acs5.get(
    #     ("NAME", "B25034_010E"), {"for": "state:{}".format(states.MD.fips)}
    # )
    # print(get)
