import os
from datetime import datetime as dt
from datetime import timedelta 

import dotenv as env

from client import TelegramClient
from custom_types import TideType
from tide_table import TideTable 

env.load_dotenv(env.find_dotenv())


def main() -> None:
    """
    Formats and sends a message about time windows in which it is possible
    to go running on, in this case, Sandy Mount Strand beach, because the tide
    is low enough.
    """
    GROUP_CHAT_ID = os.environ["group_chat_id"]
    
    """
    GPS coords of corners in which we are looking for tide data.

    See the Tide API response to understand how you need to modify this, 
    if you are interested in reporting on a different location(s).
    """
    dublin_bounding_box = [
        "-7.369079589843751", 
        "53.02965199827355", 
        "-5.061950683593751", 
        "53.66905301677406"
    ]
    dublin_name = "Dublin"

    tide_table_client = TideTable(os.environ["tide_api"])
    tide_data = tide_table_client.get(dublin_bounding_box, dublin_name)

    """Formating dates and times for Telegram message."""
    today = dt.fromtimestamp(tide_data.sunrise)
    day_name = today.strftime("%A")
    day_num = today.strftime("%d")
    month_name = today.strftime("%B")
    sunrise_time =  today.strftime("%H%M hrs")
    sunset_time = dt.fromtimestamp(tide_data.sunset).strftime("%H%M hrs")

    daily_message = f"It is {day_name}, {day_num} {month_name}.\n\n"
    daily_message += " *Low-tide window(s)*: \n\n"
    for tide_info in tide_data.tides:
        """
        Create a time window around the LOW tide in which it is
        safe to go running.

        Time delta in this case is 2 hours, as we know that in Dublin bay,
        two hours before and after low tide, the seabed is still runnable.
        Be advised that this might wildly differ for different locations.
        """
        if tide_info.type == TideType.LOW:
            ltt = dt.fromtimestamp(tide_info.timestamp)
            window_start = ltt - timedelta(hours=2, minutes=0)
            window_end = ltt + timedelta(hours=2, minutes=0)
            daily_message += f"   • {window_start.strftime('%H%M')}"
            daily_message += f" until {window_end.strftime('%H%M')} hrs\n"
    
    daily_message += f"\n 🌅 Sunrise: {sunrise_time}\n"
    daily_message += f" 🌆 Sunset: {sunset_time}\n\n"
    
    print(daily_message)

    telegram_client = TelegramClient(os.environ["api_key"])
    telegram_client.send_message(daily_message, GROUP_CHAT_ID)


if __name__ == '__main__':
    main()