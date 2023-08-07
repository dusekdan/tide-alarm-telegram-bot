import os
import re
import json
from datetime import datetime
from typing import List

import requests
import dotenv as env

from custom_types import TideInfo, TideInfoForDate, TideType

class TideTable:
    def __init__(self, api_url: str) -> None:
        self.api_url = api_url

    def get(self, 
            bounding_box: List[str] = None, 
            name: str = None, 
            date: str = None
    ) -> TideInfoForDate:
        """
        Obtains Tide information for a specific date (defaults to today).

        Args:
            bounding_box (List[str]): bounding box descriptive of the area
             for which we want to obtain the tide info. Provide 4 GPS coords
             that describe the corners of the area.
            name (str): name of the location, this value is present in the API
             response, and you have to provide the same value as is provided
             by the API. Example uses "Dublin".
            date (str): Date in `yyyy-mm-dd` format to obtain tide data for.

        Returns:
            TideInfoForDate: Information about tides for day and location.
        """
        if bounding_box is None:
            raise Exception(
                "Must provide a bounding_box: a list of 4 string integers"
            )

        if name is None:
            raise Exception(
                "Must provide a name for the location, e.g. 'Dublin'"
            )
    
        if date is None:
            date = datetime.now().isoformat(sep='T').split('T')[0]
        else:
            pattern = "2[0-9]{3}-(([0][1-9])|(1[0-2]))-[0-3][0-9]"
            if re.fullmatch(pattern, date) is None:
                raise Exception(
                    "Date must be a valid ISO date, e.g. 2023-08-06"
                )

        bounding_box_param = ",".join(bounding_box)
        url = f"{self.api_url}?bbox={bounding_box_param}"

        response = requests.get(url)
        
        if response.status_code != 200:
            raise Exception(
                f"Could not fetch tide information from {self.api_url}"
            )
        
        tide_info = json.loads(response.text)

        location_tide_info = [
            loc for loc in tide_info["locations"] if loc["name"] == name
        ]

        if len(location_tide_info) < 1:
            message = f"{name} is not present in the tide info"
            message += f" fetched from {self.api_url}"
            raise Exception(message)
    
        location_tide_info = location_tide_info[0]

        tide_info_for_date = [
            day for day in location_tide_info["days"] if day["date"] == date
        ]

        if len(tide_info_for_date) < 1:
            message = f"{date} is not present in the tide info fetched from"
            message += f"{self.api_url} for {name}"
            raise Exception(message)
        
        tide_info_for_date = tide_info_for_date[0]

        return self._map_to_tide_info_for_date(tide_info_for_date)

    def _map_to_tide_info_for_date(self, t: List) -> TideInfoForDate:
        """
        Constructs the `TideInfoForDate` object from the API response.
        """
        tides = [
            TideInfo(
            timestamp=i["timestamp"], 
            height=i["height"], 
            type=TideType.LOW if i["type"] == "low" else TideType.HIGH
            ) for i in t["tides"]
        ]

        return TideInfoForDate(
            date=t["date"], 
            sunrise=t["sunrise"], 
            sunset=t["sunset"], 
            tides=tides
        )


if __name__ == "__main__":
    env.load_dotenv(env.find_dotenv())

    tide_table = TideTable(os.environ["tide_api"])
    tide_table.get([
        "-7.369079589843751", 
        "53.02965199827355", 
        "-5.061950683593751", 
        "53.66905301677406"], 
        name="Dublin"
    )