import requests


class TelegramClient:


    send_message_api = "/sendMessage"


    def __init__(self, api_key: str) -> None:
        """
        Constructor.

        Args:
            api_key (string): API key used to authenticate to Telegram bot API.

        Returns:
            None
        """
        self.telegram_endpoint_base = f"https://api.telegram.org/bot{api_key}" 


    def send_message(self, message_body: str, chat_id: str, parse_type:str = "Markdown") -> int:
        """
        Send message to a specified chat ID, optionally choosing formatting 
        mode, defaults to markdown.

        Args:
            message_body (str): Contents of the message to be sent.
            chat_id (str): Target chat ID (should be a number in string)
            parse_type (str): defaults to `markdown`, can be `html`.
        
        Returns:
            int: Status code of Telegram API response. 
        """
        message_payload = {
            "text": message_body,
            "parse_mode": parse_type,
            "chat_id": chat_id
        }
        
        r = requests.post(
            f"{self.telegram_endpoint_base}{self.send_message_api}", 
            json=message_payload
        )

        print(f"[{r.status_code}] {r.text}")
        return r.status_code