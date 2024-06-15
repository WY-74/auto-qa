from base.web import WebKeys
from typing import Dict, Any


class BasePages(WebKeys):
    def bot(self, locators: Dict[str, Any], data_map: Dict[str, Any]):
        for key, locator in locators.items():
            option = key.split("@")[-1]
            try:
                data = data_map[key.replace(f"@{option}", "")]
            except KeyError:
                data = None

            if data is not None:
                getattr(self, option)(locator, data)
            else:
                getattr(self, option)(locator)
