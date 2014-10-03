from stagecraft.apps.dashboards.models.module import ModuleType
from dictdiffer import diff
import os
import json


def get_schema_for_module_type(name):
    path = os.path.join(
        os.path.dirname(__file__),
        'schema/dashboard.json')
    with open(path, "r") as file:
        schema = file.read()
    schema_dict = json.loads(schema)
    return schema_dict


if __name__ == '__main__':
    for module_type in ModuleType.objects.all():
        print get_schema_for_module_type(module_type.name)
