# Used to store information such as the environment address or user account/password.

import configparser
import pathlib
import json
import jsonpath

with open(f"{pathlib.Path(__file__).parent}/credentials.json") as f:
    credentials = json.load(f)

_config = configparser.ConfigParser()
_config.read('.\pytest.ini', encoding="utf-8")
_env = _config.get("credentials", "env")

credentials = jsonpath.jsonpath(credentials, f"$..{_env}")[0]
