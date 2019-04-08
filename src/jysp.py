import json
import sys

import yaml

from schema import Schema


def validate(schema_name, data_name):
    if schema_name[-4:] == '.yml':
        schema_def = yaml.load(open(schema_name))
    elif schema_name[-5:] == '.json':
        schema_def = json.load(open(schema_name))
    else:
        print('unsupported file format: {0}'.format(schema_name))
        return

    try:
        schema = Schema(schema_def)
    except Exception as e:
        print(e)

    if data_name[-4:] == '.yml':
        data_def = yaml.load(open(data_name))
    elif data_name[-5:] == '.json':
        data_def = json.load(open(data_name))
    else:
        print('unsupported file format: {0}'.format(data_name))
        return

    try:
        schema.validate(data_def)
        print('valid')
    except Exception as e:
        print(e)


if __name__ == '__main__':
    schema_name = sys.argv[1]
    data_name = sys.argv[2]
    validate(schema_name, data_name)
