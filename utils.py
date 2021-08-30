import json
from datetime import datetime
from typing import Dict


def convert_str_to_dict(text) -> Dict:
    return json.loads(text)


def convert_str_to_datetime(datetime_str: str) -> datetime:
    return datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%f%z")
