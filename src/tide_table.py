from dataclasses import dataclass
import requests
from typing import List
from collections import namedtuple
import dotenv as env
import os
import json
from datetime import datetime
import re
from enum import Enum

class TideType(Enum):
    LOW = 0
    HIGH = 1


@dataclass
class TideInfo:
    timestamp: int
    height: float
    type: TideType

@dataclass
class TideInfoForDate:
    date: str
    sunrise: int 
    sunset: int
    tides: List[TideInfo]


class TideTable:
    def __init__(self, api_url: str):
        self.api_url = api_url

    def get(self, bounding_box: List[str] = None, name: str = None, date: str = None):

        if bounding_box is None:
            raise Exception("Must provide a bounding_box: a list of 4 string integers")
        if name is None:
            raise Exception("Must provide a name for the location, e.g. 'Dublin'")
    
        if date is None:
            date = datetime.now().isoformat(sep='T').split('T')[0]
        else:
            if re.fullmatch("2[0-9]{3}-(([0][1-9])|(1[0-2]))-[0-3][0-9]", date) is None:
                raise Exception("date must be a valid ISO date, e.g. 2023-08-06")

        bounding_box_param = ",".join(bounding_box)
        url = f"{self.api_url}?bbox={bounding_box_param}"

        response = requests.get(url)
        
        if response.status_code != 200:
            raise Exception(f"could not fetch tide information from {self.api_url}")
        
        tide_info = json.loads(response.text)


        location_tide_info = [location for location in tide_info["locations"] if location["name"] == name]

        if len(location_tide_info) < 1:
            raise Exception(f"{name} is not present in the tide info fetched from {self.api_url}")
    
        location_tide_info = location_tide_info[0]

        tide_info_for_date = [day for day in location_tide_info["days"] if day["date"] == date]
        if len(tide_info_for_date) < 1:
            raise Exception(f"{date} is not present in the tide info fetched from {self.api_url} for {name}")
        tide_info_for_date = tide_info_for_date[0]

        return self._map_to_tide_info_for_date(tide_info_for_date)

    def _map_to_tide_info_for_date(self, t):
        tides = [TideInfo(timestamp=i["timestamp"], height=i["height"], type=TideType.LOW if i["type"] == "low" else TideType.HIGH) for i in t["tides"]]

        return TideInfoForDate(date=t["date"], sunrise=t["sunrise"], sunset=t["sunset"], tides=tides)

if __name__ == "__main__":
    env.load_dotenv(env.find_dotenv())

    tide_table = TideTable(os.environ["tide_api"])

    tide_table.get(["-7.369079589843751", "53.02965199827355", "-5.061950683593751", "53.66905301677406"], name="Dublin")