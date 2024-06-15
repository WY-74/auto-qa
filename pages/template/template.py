from typing import Dict, Any
from pages.base_pages import BasePages


class Template(BasePages):
    def run(self, locators: Dict[str, Any], data_map: Dict[str, Any]):
        self.navigate("https://www.baidu.com")
        self.bot(locators, data_map)
