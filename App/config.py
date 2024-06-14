import json

def load_config():
    with open("config.json", encoding="utf-8") as f:
        return json.load(f)

config = load_config()
