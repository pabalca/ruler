import sys
import json
import requests
import logging


class Alert:
    def __init__(self):
        self.api = "https://api.telegram.org/"
        self.token = "bot5639894858:AAHQqUs9rElHA1ns6vsWz0-esObpHM47OCg"
        self.chat_id = "716400002"


    def send_message(self, message):
        try:
            r = requests.post(
                self.api + self.token + "/sendMessage",
                params={"chat_id": self.chat_id, "text": message},
            )
        except Exception as e:
            logging.error(f"Exception {e}")
            sys.exit()

        if r.json()["ok"]:
            logging.info(f"Alert {message} sent")
            return True
        else:
            logging.error(f"Failed to send alert {message}")
            return False
