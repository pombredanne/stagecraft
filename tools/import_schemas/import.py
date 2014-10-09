#!/usr/bin/env python
# encoding: utf-8

from stagecraft.apps.dashboards.models.module import(
    ModuleType,
    Module)
from dictdiffer import diff
import os
import json
import pprint
import jsonschema

# run it like this:
# workon/source the virtualenv
# run export DJANGO_SETTINGS_MODULE=stagecraft.settings.production
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


def check_module_type_schemas_correct():
    all_correct = True
    for module_type, new_schema in module_types_with_proper_schemas():
        diffs = list(diff(module_type.schema, new_schema))
        print "==============={}========================".format(module_type.name)
        if len(diffs) != 0:
            all_correct = False
            print '{} differs'.format(module_type.name)
            pprint.pprint(diffs)
            print "NOT YET THE SAME!"
        else:
            print "SCHEMA OKAY"
        print "======================================="
        try:
            module_type.validate_schema()
        except jsonschema.exceptions.SchemaError as e:
            print "==============="
            print module_type.name
            print "==============="
            raise e
    return all_correct


def clear_module_type_schemas():
    for module_type, new_schema in module_types_with_proper_schemas():
        update_module_type_schema(module_type, schema={})


def update_module_type_with_correct_schemas():
    for module_type, new_schema in module_types_with_proper_schemas():
        update_module_type_schema(module_type, schema=new_schema)


def update_module_type_schema(module_type, schema={}):
    module_type.schema = schema
    module_type.save()


def module_types_with_proper_schemas():
    module_types_with_proper_schemas = [
        (module_type, get_schema_for_module_type(module_type.name))
        for module_type in ModuleType.objects.all()
    ]
    return module_types_with_proper_schemas


def validate_all_modules():
    for module in Module.objects.all():
    #    import pdb; pdb.set_trace()
        jsonschema.validate(module.options, module.type.schema)
        print "MODULE OKAY!"
        return True

if __name__ == '__main__':
    clear_module_type_schemas()
    check_module_type_schemas_correct()
    update_module_type_with_correct_schemas()
    all_correct = check_module_type_schemas_correct()
    if all_correct:
        validate_all_modules()
    print "what happens with dashboards.json yeah?"
