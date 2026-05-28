"""
JSON File Storage for Account Data
"""

import json
import os


class Storage:
    DATA_FILE = "data/accounts.json"

    def __init__(self):
        os.makedirs(os.path.dirname(self.DATA_FILE), exist_ok=True)

    def load(self):
        if not os.path.exists(self.DATA_FILE):
            return {}
        try:
            with open(self.DATA_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}

    def save(self, data):
        with open(self.DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)
