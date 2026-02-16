"""
This module connects to Django models using the load_django import,
reads the json file and writes to the postgres database.
"""

import json
from load_django import *
from parser_app.models import Product


def push_db():
    with open("../files/parse_data_brain.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        obj, create = Product.objects.get_or_create(**data)
        print(f"{obj}, {create}")


if __name__ == "__main__":
    push_db()
