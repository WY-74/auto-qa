import requests
import jsonpath
from typing import Dict, List, Any
from config.log import logger


class ApiKeys:
    def __init__(self, url: str = None) -> None:
        self.url = url
        self.logger = logger
        self.logger.info("init apikeys finished")

    def get(
        self, path: str = None, params: Dict[str, Any] | None = None, headers: Dict[str, Any] | None = None, **kwargs
    ):
        return requests.get(url=f"{self.url}/{path}", params=params, headers=headers, **kwargs)

    def post(
        self,
        path: str = None,
        data: Dict[str, Any] | None = None,
        headers: Dict[str, Any] | None = None,
        with_json: bool = True,
        **kwargs,
    ):
        if with_json:
            return requests.post(url=f"{self.url}/{path}", json=data, headers=headers, **kwargs)
        return requests.post(url=f"{self.url}/{path}", data=data, headers=headers, **kwargs)

    def get_values_from_json(response, key) -> List[Any]:
        expr = f"$..{key}"

        return jsonpath(response, expr)
