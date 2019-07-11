import json
import os
from typing import Optional, List

DATA_DIR = './data'
ACTIVITIES_FN = "activities.json"
CATEGORIES_FN = "categories.json"


def save(file_name: str, data: str):
    if not os.path.exists(DATA_DIR):
        os.mkdir(DATA_DIR)
    with open(f'{DATA_DIR}/{file_name}', 'w') as f:
        f.write(data)


def read(file_name: str) -> Optional[str]:
    if not os.path.exists(f'{DATA_DIR}/{file_name}'):
        return

    with open(f'{DATA_DIR}/{file_name}', 'r') as f:
        return ''.join(f.readlines())


def load_categories() -> List:
    categories_str = read(CATEGORIES_FN)
    if not categories_str:
        categories_str = '[]'
    return json.loads(categories_str)


def load_activities() -> List:
    activities_str = read(ACTIVITIES_FN)
    if not activities_str:
        activities_str = '[]'
    return json.loads(activities_str)