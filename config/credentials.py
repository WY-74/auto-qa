# Used to store information such as the environment address or user account/password.

import configparser

credentials = {
    "dev": {},
    "qa": {},
    "main": {},
}

_config = configparser.ConfigParser()
_config.read('.\pytest.ini', encoding="utf-8")

credentials = credentials[_config.get("credentials", "env")]
