#!/usr/bin/env python
# encoding: utf-8

from stagecraft.apps.dashboards.models.module import ModuleType
from dictdiffer import diff
import os
import json

# run it like this:
# python -m tools.import_schemas.import


def get_schema_for_module_type(name):
    path = os.path.join(
        os.path.dirname(__file__),
        'schema/modules_json/{}_schema.json'.format(name))
    try:
        with open(path, "r") as file:
            schema = file.read()
    except IOError as e:
        path = os.path.join(
            os.path.dirname(__file__),
            'schema/module.json'.format(name))
        with open(path, "r") as file:
            schema = file.read()
    schema_dict = json.loads(schema)
    return schema_dict


if __name__ == '__main__':
    for module_type in ModuleType.objects.all():
        get_schema_for_module_type(module_type.name)
