from typing import List, Any
from jsonpath import jsonpath


def get_values_from_json(data, key) -> List[Any]:
    expr = f"$..{key}"

    return jsonpath(data, expr)
