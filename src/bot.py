from typing import List
import os
import requests
import json
import dotenv as env

from client import TelegramClient

env.load_dotenv(env.find_dotenv())

class TideAlarmBot:

    def __init__(self):
        pass


def main():
    pass


if __name__ == '__main__':
    main()

    GROUP_CHAT_ID = os.environ["group_chat_id"]

    telegram_client = TelegramClient(os.environ["api_key"])
    telegram_client.send_message("Please accept this humble message.", GROUP_CHAT_ID)