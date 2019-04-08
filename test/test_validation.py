import unittest
import os
import sys

import yaml

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from error import ValidationError   # pylint: disable=no-name-in-module, wrong-import-position
from schema import Schema           # pylint: disable=import-error, wrong-import-position


class TestValidation(unittest.TestCase):
    def setUp(self):
        data_file_name = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                      'data/validation.yml'))
        with open(data_file_name) as validation_data:
            self.test_data = yaml.load(validation_data)

    def test_bool(self):
        test_case_name = 'bool'
        schema = Schema(self.test_data[test_case_name]['schema'])
        data = self.test_data[test_case_name]['data']
        self.assertTrue(schema.validate(data))

    def test_string(self):
        test_case_name = 'string'
        schema = Schema(self.test_data[test_case_name]['schema'])
        data = self.test_data[test_case_name]['data']
        self.assertTrue(schema.validate(data))

    def test_int(self):
        test_case_name = 'int'
        schema = Schema(self.test_data[test_case_name]['schema'])
        data = self.test_data[test_case_name]['data']
        self.assertTrue(schema.validate(data))

    def test_float(self):
        test_case_name = 'float'
        schema = Schema(self.test_data[test_case_name]['schema'])
        data = self.test_data[test_case_name]['data']
        self.assertTrue(schema.validate(data))

    def test_not_bool(self):
        test_case_name = 'not_bool'
        schema = Schema(self.test_data[test_case_name]['schema'])
        data = self.test_data[test_case_name]['data']
        with self.assertRaises(ValidationError) as context:
            schema.validate(data)
        self.assertEqual(context.exception.msg, 'Expected type: bool')
        self.assertEqual(context.exception.path, 'logical')

    def test_not_string(self):
        test_case_name = 'not_string'
        schema = Schema(self.test_data[test_case_name]['schema'])
        data = self.test_data[test_case_name]['data']
        with self.assertRaises(ValidationError) as context:
            schema.validate(data)
        self.assertEqual(context.exception.msg, 'Expected type: string')
        self.assertEqual(context.exception.path, 'text')

    def test_not_int(self):
        test_case_name = 'not_int'
        schema = Schema(self.test_data[test_case_name]['schema'])
        data = self.test_data[test_case_name]['data']
        with self.assertRaises(ValidationError) as context:
            schema.validate(data)
        self.assertEqual(context.exception.msg, 'Expected type: int')
        self.assertEqual(context.exception.path, 'number')

    def test_not_float(self):
        test_case_name = 'not_float'
        schema = Schema(self.test_data[test_case_name]['schema'])
        data = self.test_data[test_case_name]['data']
        with self.assertRaises(ValidationError) as context:
            schema.validate(data)
        self.assertEqual(context.exception.msg, 'Expected type: float')
        self.assertEqual(context.exception.path, 'value')

    def test_simple_map(self):
        test_case_name = 'simple_map'
        schema = Schema(self.test_data[test_case_name]['schema'])
        data = self.test_data[test_case_name]['data']
        self.assertTrue(schema.validate(data))

    def test_map_is_not_map(self):
        test_case_name = 'map_is_not_map'
        schema = Schema(self.test_data[test_case_name]['schema'])
        data = self.test_data[test_case_name]['data']
        with self.assertRaises(ValidationError) as context:
            schema.validate(data)
        self.assertEqual(context.exception.msg, 'Expected type: map')
        self.assertEqual(context.exception.path, 'person')

    def test_map_item_wrong_type(self):
        test_case_name = 'map_item_wrong_type'
        schema = Schema(self.test_data[test_case_name]['schema'])
        data = self.test_data[test_case_name]['data']
        with self.assertRaises(ValidationError) as context:
            schema.validate(data)
        self.assertEqual(context.exception.msg, 'Expected type: int')
        self.assertEqual(context.exception.path, 'person.age')

    def test_unexpected_map_item(self):
        test_case_name = 'unexpected_map_item'
        schema = Schema(self.test_data[test_case_name]['schema'])
        data = self.test_data[test_case_name]['data']
        with self.assertRaises(ValidationError) as context:
            schema.validate(data)
        self.assertEqual(context.exception.msg, 'Unexpected item: "eye_color"')
        self.assertEqual(context.exception.path, 'person')

    def test_missing_map_item(self):
        test_case_name = 'missing_map_item'
        schema = Schema(self.test_data[test_case_name]['schema'])
        data = self.test_data[test_case_name]['data']
        with self.assertRaises(ValidationError) as context:
            schema.validate(data)
        self.assertEqual(context.exception.msg, 'Missing required item: "age"')
        self.assertEqual(context.exception.path, 'person')

    def test_optional_component_is_missing(self):
        test_case_name = 'optional_component_is_missing'
        schema = Schema(self.test_data[test_case_name]['schema'])
        data = self.test_data[test_case_name]['data']
        self.assertTrue(schema.validate(data))

    def test_optional_map_item_is_missing(self):
        test_case_name = 'optional_map_item_is_missing'
        schema = Schema(self.test_data[test_case_name]['schema'])
        data = self.test_data[test_case_name]['data']
        self.assertTrue(schema.validate(data))

    def test_complex_map(self):
        test_case_name = 'complex_map'
        schema = Schema(self.test_data[test_case_name]['schema'])
        data = self.test_data[test_case_name]['data']
        self.assertTrue(schema.validate(data))

    def test_recursive_map(self):
        test_case_name = 'recursive_map'
        schema = Schema(self.test_data[test_case_name]['schema'])
        data = self.test_data[test_case_name]['data']
        self.assertTrue(schema.validate(data))

    def test_simple_list(self):
        test_case_name = 'simple_list'
        schema = Schema(self.test_data[test_case_name]['schema'])
        data = self.test_data[test_case_name]['data']
        self.assertTrue(schema.validate(data))

    def test_list_unexpected_type(self):
        test_case_name = 'list_unexpected_type'
        schema = Schema(self.test_data[test_case_name]['schema'])
        data = self.test_data[test_case_name]['data']
        with self.assertRaises(ValidationError) as context:
            schema.validate(data)
        self.assertEqual(context.exception.msg, 'Unexpected type: "string"')
        self.assertEqual(context.exception.path, 'sequence')

    def test_list_too_few(self):
        test_case_name = 'list_too_few'
        schema = Schema(self.test_data[test_case_name]['schema'])
        data = self.test_data[test_case_name]['data']
        with self.assertRaises(ValidationError) as context:
            schema.validate(data)
        self.assertEqual(context.exception.msg, 'Too few list items: min=4')
        self.assertEqual(context.exception.path, 'sequence')

    def test_list_too_many(self):
        test_case_name = 'list_too_many'
        schema = Schema(self.test_data[test_case_name]['schema'])
        data = self.test_data[test_case_name]['data']
        with self.assertRaises(ValidationError) as context:
            schema.validate(data)
        self.assertEqual(context.exception.msg, 'Too many list items: max=2')
        self.assertEqual(context.exception.path, 'sequence')


if __name__ == '__main__':
    unittest.main()
