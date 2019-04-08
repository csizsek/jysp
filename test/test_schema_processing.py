import unittest
import os
import sys

import yaml

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from descriptor import BoolDescriptor, IntDescriptor, FloatDescriptor, StringDescriptor, MapDescriptor, ListDescriptor # pylint: disable=import-error, wrong-import-position, line-too-long
from error import SchemaError       # pylint: disable=no-name-in-module, wrong-import-position
from schema import Schema           # pylint: disable=import-error, wrong-import-position


class TestSchemaProcessing(unittest.TestCase):

    def setUp(self):
        data_file_name = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                      'data/schema_processing.yml'))
        with open(data_file_name) as schema_processing_data:
            self.test_data = yaml.load(schema_processing_data)

    def test_empty_schema(self):
        test_case_name = 'empty_schema'
        with self.assertRaises(SchemaError) as context:
            Schema(self.test_data[test_case_name]['schema'])
        self.assertEqual(context.exception.msg, 'No component definitions found')

    def test_definitions_part_is_not_a_map(self):
        test_case_name = 'definitions_part_is_not_a_map'
        with self.assertRaises(SchemaError) as context:
            Schema(self.test_data[test_case_name]['schema'])
        self.assertEqual(context.exception.msg, 'Incorrect schema type')

    def test_component_has_no_definition(self):
        test_case_name = 'component_has_no_definition'
        with self.assertRaises(SchemaError) as context:
            Schema(self.test_data[test_case_name]['schema'])
        self.assertEqual(context.exception.msg, 'The component has no definition')

    def test_component_definition_is_not_a_map(self):
        test_case_name = 'component_definition_is_not_a_map'
        with self.assertRaises(SchemaError) as context:
            Schema(self.test_data[test_case_name]['schema'])
        self.assertEqual(context.exception.msg,
                         'The component definition is not of type "map"')

    def test_component_has_no_type(self):
        test_case_name = 'component_has_no_type'
        with self.assertRaises(SchemaError) as context:
            Schema(self.test_data[test_case_name]['schema'])
        self.assertEqual(context.exception.msg, 'The component has no type')

    def test_component_type_is_not_a_string(self):
        test_case_name = 'component_type_is_not_a_string'
        with self.assertRaises(SchemaError) as context:
            Schema(self.test_data[test_case_name]['schema'])
        self.assertEqual(context.exception.msg,
                         'The component type attribute is not a type name')

    def test_component_type_unknown(self):
        test_case_name = 'component_type_unknown'
        with self.assertRaises(SchemaError) as context:
            Schema(self.test_data[test_case_name]['schema'])
        self.assertEqual(context.exception.msg, 'Unknown type: "hello"')

    def test_component_type_bool(self):
        test_case_name = 'component_type_bool'
        schema = Schema(self.test_data[test_case_name]['schema'])
        self.assertTrue(isinstance(schema.descriptors['logical'],
                                   BoolDescriptor))
        self.assertEqual(len(schema.descriptors), 5)

    def test_component_type_string(self):
        test_case_name = 'component_type_string'
        schema = Schema(self.test_data[test_case_name]['schema'])
        self.assertTrue(isinstance(schema.descriptors['text'], StringDescriptor))
        self.assertEqual(len(schema.descriptors), 5)

    def test_component_type_int(self):
        test_case_name = 'component_type_int'
        schema = Schema(self.test_data[test_case_name]['schema'])
        self.assertTrue(isinstance(schema.descriptors['number'], IntDescriptor))
        self.assertEqual(len(schema.descriptors), 5)

    def test_component_type_float(self):
        test_case_name = 'component_type_float'
        schema = Schema(self.test_data[test_case_name]['schema'])
        self.assertTrue(isinstance(schema.descriptors['number'],
                                   FloatDescriptor))
        self.assertEqual(len(schema.descriptors), 5)

    def test_map_has_no_items_component(self):
        test_case_name = 'map_has_no_items_component'
        with self.assertRaises(SchemaError) as context:
            Schema(self.test_data[test_case_name]['schema'])
        self.assertEqual(context.exception.msg, 'No component definitions found')

    def test_map_has_none_items_component(self):
        test_case_name = 'map_has_none_items_component'
        with self.assertRaises(SchemaError) as context:
            Schema(self.test_data[test_case_name]['schema'])
        self.assertEqual(context.exception.msg, 'No component definitions found')

    def test_map_items_component_is_not_a_list(self):
        test_case_name = 'map_items_component_is_not_a_list'
        with self.assertRaises(SchemaError) as context:
            Schema(self.test_data[test_case_name]['schema'])
        self.assertEqual(context.exception.msg, 'Component items definition '
                         'list is not of type "list"')

    def test_map_has_empty_items_component(self):
        test_case_name = 'map_has_empty_items_component'
        with self.assertRaises(SchemaError) as context:
            Schema(self.test_data[test_case_name]['schema'])
        self.assertEqual(context.exception.msg, 'No component definitions found')

    def test_map_item_is_none(self):
        test_case_name = 'map_item_is_none'
        with self.assertRaises(SchemaError) as context:
            Schema(self.test_data[test_case_name]['schema'])
        self.assertEqual(context.exception.msg, 'Component is None')

    def test_map_item_is_not_a_map(self):
        test_case_name = 'map_item_is_not_a_map'
        with self.assertRaises(SchemaError) as context:
            Schema(self.test_data[test_case_name]['schema'])
        self.assertEqual(context.exception.msg,
                         'The component definition is not of type "map"')

    def test_map_item_is_empty(self):
        test_case_name = 'map_item_is_empty'
        with self.assertRaises(SchemaError) as context:
            Schema(self.test_data[test_case_name]['schema'])
        self.assertEqual(context.exception.msg, 'Component is empty')

    def test_map_item_has_no_definition(self):
        test_case_name = 'map_item_has_no_definition'
        with self.assertRaises(SchemaError) as context:
            Schema(self.test_data[test_case_name]['schema'])
        self.assertEqual(context.exception.msg, 'The component has no definition')

    def test_map_item_has_no_type(self):
        test_case_name = 'map_item_has_no_type'
        with self.assertRaises(SchemaError) as context:
            Schema(self.test_data[test_case_name]['schema'])
        self.assertEqual(context.exception.msg, 'The component has no type')

    def test_map_item_has_unknown_type(self):
        test_case_name = 'map_item_has_unknown_type'
        with self.assertRaises(SchemaError) as context:
            Schema(self.test_data[test_case_name]['schema'])
        self.assertEqual(context.exception.msg, 'Unknown type: "text"')

    def test_map_item_required_is_not_a_bool(self):
        test_case_name = 'map_item_required_is_not_a_bool'
        with self.assertRaises(SchemaError) as context:
            Schema(self.test_data[test_case_name]['schema'])
        self.assertEqual(context.exception.msg,
                         'The required attribute is not of type "bool"')

    def test_simple_map_type(self):
        test_case_name = 'simple_map_type'
        schema = Schema(self.test_data[test_case_name]['schema'])
        self.assertTrue(isinstance(schema.descriptors['person'], MapDescriptor))
        self.assertEqual(len(schema.descriptors), 5)

    def test_alias_map_type(self):
        test_case_name = 'alias_map_type'
        schema = Schema(self.test_data[test_case_name]['schema'])
        self.assertTrue(isinstance(schema.descriptors['person'], MapDescriptor))
        self.assertTrue(isinstance(schema.descriptors['human'], MapDescriptor))
        self.assertEqual(len(schema.descriptors), 6)

    def test_map_item_has_map_type(self):
        test_case_name = 'map_item_has_map_type'
        schema = Schema(self.test_data[test_case_name]['schema'])
        self.assertTrue(isinstance(schema.descriptors['person'], MapDescriptor))
        self.assertTrue(isinstance(schema.descriptors['person.name'],
                                   MapDescriptor))
        self.assertEqual(len(schema.descriptors), 6)

    def test_map_contains_unknown_type(self):
        test_case_name = 'map_contains_unknown_type'
        with self.assertRaises(SchemaError) as context:
            Schema(self.test_data[test_case_name]['schema'])
        self.assertEqual(context.exception.msg, 'Unknown type: "vehicle"')

    def test_deep_map(self):
        test_case_name = 'deep_map'
        schema = Schema(self.test_data[test_case_name]['schema'])
        self.assertTrue(isinstance(schema.descriptors['person'], MapDescriptor))
        self.assertTrue(isinstance(schema.descriptors['person.name'],
                                   MapDescriptor))
        self.assertTrue(isinstance(schema.descriptors['person.name.hello'],
                                   MapDescriptor))
        self.assertEqual(len(schema.descriptors), 7)

    def test_map_item_has_predefined_type(self):
        test_case_name = 'map_item_has_predefined_type'
        schema = Schema(self.test_data[test_case_name]['schema'])
        self.assertTrue(isinstance(schema.descriptors['person'], MapDescriptor))
        self.assertTrue(isinstance(schema.descriptors['animal'], MapDescriptor))
        self.assertEqual(len(schema.descriptors), 6)

    def test_map_is_recursive(self):
        test_case_name = 'map_is_recursive'
        schema = Schema(self.test_data[test_case_name]['schema'])
        self.assertTrue(isinstance(schema.descriptors['node'], MapDescriptor))
        self.assertEqual(len(schema.descriptors), 5)

    def test_mutually_recursive_maps(self):
        test_case_name = 'mutually_recursive_maps'
        schema = Schema(self.test_data[test_case_name]['schema'])
        self.assertTrue(isinstance(schema.descriptors['a'], MapDescriptor))
        self.assertTrue(isinstance(schema.descriptors['b'], MapDescriptor))
        self.assertEqual(len(schema.descriptors), 6)

    def test_list_has_no_item_types_component(self):
        test_case_name = 'list_has_no_item_types_component'
        with self.assertRaises(SchemaError) as context:
            Schema(self.test_data[test_case_name]['schema'])
        self.assertEqual(context.exception.msg,
                         'The component has no "item_types" list')

    def test_list_has_none_item_types_component(self):
        test_case_name = 'list_has_none_item_types_component'
        with self.assertRaises(SchemaError) as context:
            Schema(self.test_data[test_case_name]['schema'])
        self.assertEqual(context.exception.msg,
                         'The component has no "item_types" list')

    def test_list_item_types_component_is_not_a_list(self):
        test_case_name = 'list_item_types_component_is_not_a_list'
        with self.assertRaises(SchemaError) as context:
            Schema(self.test_data[test_case_name]['schema'])
        self.assertEqual(context.exception.msg,
                         'The item types definition is not of type "list"')

    def test_list_item_types_component_is_empty_list(self):
        test_case_name = 'list_item_types_component_is_empty_list'
        with self.assertRaises(SchemaError) as context:
            Schema(self.test_data[test_case_name]['schema'])
        self.assertEqual(context.exception.msg,
                         'The component has empty "item_types" list')

    def test_simple_list(self):
        test_case_name = 'simple_list'
        schema = Schema(self.test_data[test_case_name]['schema'])
        self.assertTrue(isinstance(schema.descriptors['sequence'],
                                   ListDescriptor))
        self.assertEqual(len(schema.descriptors), 5)

    def test_multitype_list(self):
        test_case_name = 'multitype_list'
        schema = Schema(self.test_data[test_case_name]['schema'])
        self.assertTrue(isinstance(schema.descriptors['sequence'],
                                   ListDescriptor))
        self.assertEqual(len(schema.descriptors), 5)

    def test_list_min_not_int(self):
        test_case_name = 'list_min_not_int'
        with self.assertRaises(SchemaError) as context:
            Schema(self.test_data[test_case_name]['schema'])
        self.assertEqual(context.exception.msg,
                         'The min attribute is not of type "int"')

    def test_list_min_negative(self):
        test_case_name = 'list_min_negative'
        with self.assertRaises(SchemaError) as context:
            Schema(self.test_data[test_case_name]['schema'])
        self.assertEqual(context.exception.msg,
                         'The min attribute is not a non-negative integer')

    def test_list_min(self):
        test_case_name = 'list_min'
        schema = Schema(self.test_data[test_case_name]['schema'])
        self.assertTrue(isinstance(schema.descriptors['sequence'],
                                   ListDescriptor))
        self.assertEqual(len(schema.descriptors), 5)

    def test_list_max_not_int(self):
        test_case_name = 'list_max_not_int'
        with self.assertRaises(SchemaError) as context:
            Schema(self.test_data[test_case_name]['schema'])
        self.assertEqual(context.exception.msg,
                         'The max attribute is not of type "int"')

    def test_list_max_negative(self):
        test_case_name = 'list_max_negative'
        with self.assertRaises(SchemaError) as context:
            Schema(self.test_data[test_case_name]['schema'])
        self.assertEqual(context.exception.msg,
                         'The max attribute is not a non-negative integer')

    def test_list_max(self):
        test_case_name = 'list_max'
        schema = Schema(self.test_data[test_case_name]['schema'])
        self.assertTrue(isinstance(schema.descriptors['sequence'],
                                   ListDescriptor))
        self.assertEqual(len(schema.descriptors), 5)

    def test_list_min_greater_than_max(self):
        test_case_name = 'list_min_greater_than_max'
        with self.assertRaises(SchemaError) as context:
            Schema(self.test_data[test_case_name]['schema'])
        self.assertEqual(context.exception.msg,
                         'The min attribute is greatr than max')

    def test_list_min_max(self):
        test_case_name = 'list_min_max'
        schema = Schema(self.test_data[test_case_name]['schema'])
        self.assertTrue(isinstance(schema.descriptors['sequence'],
                                   ListDescriptor))
        self.assertEqual(len(schema.descriptors), 5)

    def test_list_contains_unknown_type(self):
        test_case_name = 'list_contains_unknown_type'
        with self.assertRaises(SchemaError) as context:
            Schema(self.test_data[test_case_name]['schema'])
        self.assertEqual(context.exception.msg, 'Unknown type: "person"')

    def test_list_contains_predefined_type(self):
        test_case_name = 'list_contains_predefined_type'
        schema = Schema(self.test_data[test_case_name]['schema'])
        self.assertTrue(isinstance(schema.descriptors['sequence'],
                                   ListDescriptor))
        self.assertTrue(isinstance(schema.descriptors['person'], MapDescriptor))
        self.assertEqual(len(schema.descriptors), 6)

    def test_complex(self):
        test_case_name = 'complex'
        schema = Schema(self.test_data[test_case_name]['schema'])
        self.assertTrue(isinstance(schema.descriptors['dog'], MapDescriptor))
        self.assertTrue(isinstance(schema.descriptors['person'], MapDescriptor))
        self.assertTrue(isinstance(schema.descriptors['text'], StringDescriptor))
        self.assertTrue(isinstance(schema.descriptors['number'], IntDescriptor))
        self.assertTrue(isinstance(schema.descriptors['logical'],
                                   BoolDescriptor))
        self.assertTrue(isinstance(schema.descriptors['node'], MapDescriptor))
        self.assertTrue(isinstance(schema.descriptors['book'], MapDescriptor))
        self.assertTrue(isinstance(schema.descriptors['library'],
                                   ListDescriptor))
        self.assertTrue(isinstance(schema.descriptors['outermap'],
                                   MapDescriptor))
        self.assertTrue(isinstance(schema.descriptors['outermap.innermap'],
                                   MapDescriptor))
        self.assertTrue(isinstance(schema.descriptors['student'], MapDescriptor))
        self.assertTrue(isinstance(schema.descriptors['school'], MapDescriptor))
        self.assertTrue(isinstance(schema.descriptors['person.pets'],
                                   ListDescriptor))
        self.assertTrue(isinstance(schema.descriptors['school.students'],
                                   ListDescriptor))
        self.assertTrue(isinstance(schema.descriptors['student.schools'],
                                   ListDescriptor))
        self.assertEqual(len(schema.descriptors), 19)

    def test_complex2(self):
        test_case_name = 'complex2'
        schema = Schema(self.test_data[test_case_name]['schema'])
        self.assertTrue(isinstance(schema.descriptors['book'], MapDescriptor))
        self.assertTrue(isinstance(schema.descriptors['city'], MapDescriptor))
        self.assertTrue(isinstance(schema.descriptors['city.library'],
                                   MapDescriptor))
        self.assertTrue(isinstance(schema.descriptors['city.library.books'],
                                   ListDescriptor))
        self.assertEqual(len(schema.descriptors), 8)


if __name__ == '__main__':
    unittest.main()
