"""
This module contains the class that represents the schema of the documents and the necessary utility
methods for loading, processing and validating the documents agains the schema. The logic of the
schema processing relies upon the lower-level descriptor classes defined in the descriptors module.
"""

from typing import Any, Dict, List, Tuple, Optional

from descriptor import Descriptor, IncompleteTypeDescriptor, BoolDescriptor, IntDescriptor,\
    FloatDescriptor, StringDescriptor, MapItem, MapDescriptor, ListDescriptor   # pylint: disable=import-error, wrong-import-position, line-too-long
from error import SchemaError   # pylint: disable=no-name-in-module, wrong-import-position


class Schema:
    """
    This class represents the schema of the json/yaml documents and is capable of loading, storing
    and validating schemas according to a schema definition.
    """
    def __init__(self,
                 schema_def: Dict[str, Dict]):
        """
        Constructor for the Schema class which takes a schema definition and stores

        :param schema_def: The definition of a schema as a dict.
        """
        self.schema_def: Dict[str, Any] = {}
        self.schema_def['type'] = 'map'
        self.schema_def['required'] = True
        self.schema_def['items'] = []
        if schema_def is None:
            raise SchemaError('', 'No component definitions found')
        if not isinstance(schema_def, dict):
            raise SchemaError('', 'Incorrect schema type')
        if not schema_def:
            raise SchemaError('', 'No component definitions found')
        for name in schema_def:
            self.schema_def['items'].append({name: schema_def[name]})
        self.primitive_types = ['bool', 'string', 'int', 'float']
        self.descriptors: Dict[str, Descriptor] = {}
        self.descriptors['bool'] = BoolDescriptor()
        self.descriptors['string'] = StringDescriptor()
        self.descriptors['int'] = IntDescriptor()
        self.descriptors['float'] = FloatDescriptor()
        self.schema = self.create_map_descriptor('__schema__', self.schema_def, [])

    def register_descriptor(self,    # pylint: disable=too-many-branches
                            component_name: str,
                            component_def: Optional[Dict[str, Any]],
                            path: List[str])\
            -> Tuple[str, bool]:
        """
        This method registers a descriptor (i.e. adds it) to the schema. The details of this new
        descriptor (name, definition, path) are specified by the arguments of the method.

        :param component_name: The name of the component to be registered.
        :param component_def: The definition of the component to be registered.
        :param path: The path of the component to be registered.
        :return: A two-tuple consisting of the component type and a boolean that is True if it is a
            required component.
        """
        if component_def is None:
            raise SchemaError('.'.join(path), 'The component has no definition')
        if not isinstance(component_def, dict):
            raise SchemaError('.'.join(path), 'The component definition is not of type "map"')
        if 'type' not in component_def:
            raise SchemaError('.'.join(path), 'The component has no type')
        component_type = component_def['type']
        if not isinstance(component_type, str):
            raise SchemaError('.'.join(path), 'The component type attribute is not a type name')
        component_required = True
        if 'required' in component_def:
            component_required = component_def['required']
        if not isinstance(component_required, bool):
            raise SchemaError('.'.join(path), 'The required attribute is not of type "bool"')
        if component_name in self.descriptors:
            pass
        elif component_type in self.primitive_types:
            if not path:
                self.descriptors[component_name] = self.descriptors[component_type]
        elif component_type == 'map':
            generated_type_name = component_name
            if path:
                generated_type_name = '.'.join(path + [component_name])
            self.descriptors[generated_type_name] = self.create_map_descriptor(component_name,
                                                                               component_def,
                                                                               path)
            component_type = generated_type_name
        elif component_type == 'list':
            component_type = '.'.join(path + [component_name])
            self.descriptors[component_type] = self.create_list_descriptor(
                component_name, component_def, path)
        elif self.get_definition(component_type):
            self.descriptors[component_name] = IncompleteTypeDescriptor()
            self.register_descriptor(component_type, self.get_definition(component_type), [])
            if not path:
                self.descriptors[component_name] = self.descriptors[component_type]
        else:
            raise SchemaError('.'.join(path), 'Unknown type: "{0}"'.format(component_type))
        if component_name in self.descriptors and isinstance(
                self.descriptors[component_name], IncompleteTypeDescriptor):
            del self.descriptors[component_name]
        return (component_type, component_required)

    def create_map_descriptor(self,
                              component_name: str,
                              component_def: Dict[str, Any],
                              path: List[str])\
            -> MapDescriptor:
        """
        This method returns a MapDescriptor with the details specified in the arguments.

        :param component_name: The name of the component to be created.
        :param component_def: The definition of the component to be created.
        :param path: The path of the component to be created.
        :return: A MapDescriptor instance describing the new component.
        """
        if 'items' not in component_def:
            raise SchemaError('.'.join(path), 'No component definitions found')
        items = component_def['items']
        if items is None:
            raise SchemaError('.'.join(path), 'No component definitions found')
        if not isinstance(items, list):
            raise SchemaError('.'.join(path), 'Component items definition '
                                              'list is not of type "list"')
        if not items:
            raise SchemaError('.'.join(path), 'No component definitions found')
        map_items = []
        for item in items:
            if item is None:
                raise SchemaError('.'.join(path), 'Component is None')
            if not isinstance(item, dict):
                raise SchemaError('.'.join(path), 'The component definition is not of type "map"')
            if not item:
                raise SchemaError('.'.join(path), 'Component is empty')
            for item_name in item:
                item_components = item[item_name]
                if component_name != '__schema__':
                    path.append(component_name)
                item_type, item_required = self.register_descriptor(
                    item_name, item_components, path)
                map_items.append(MapItem(item_name, item_type, item_required))
                if component_name != '__schema__':
                    path.pop()
        return MapDescriptor(map_items, self.descriptors)

    def create_list_descriptor(self,    # pylint: disable=too-many-branches
                               component_name: str,
                               component_def: Dict[str, Any],
                               path: List[str])\
            -> ListDescriptor:
        """
        This method returns a ListDescriptor with the details specified in the arguments.

        :param component_name: The name of the component to be created.
        :param component_def: The definition of the component to be created.
        :param path: The path of the component to be created.
        :return: A ListDescriptor instance describing the new component.
        """
        if 'item_types' not in component_def:
            raise SchemaError('.'.join(path), 'The component has no "item_types" list')
        item_types = component_def['item_types']
        if item_types is None:
            raise SchemaError('.'.join(path), 'The component has no "item_types" list')
        if not isinstance(item_types, list):
            raise SchemaError('.'.join(path), 'The item types definition is not of type "list"')
        if not item_types:
            raise SchemaError('.'.join(path), 'The component has empty "item_types" list')
        for item_type in item_types:
            if item_type not in self.descriptors:
                if self.get_definition(item_type):
                    self.descriptors[component_name] = IncompleteTypeDescriptor()
                    self.register_descriptor(item_type, self.get_definition(item_type), [])
                else:
                    raise SchemaError('.'.join(path), 'Unknown type: "{0}"'.format(item_type))
        min_items = None
        if 'min' in component_def:
            min_items = component_def['min']
        if min_items is not None and not isinstance(min_items, int):
            raise SchemaError('.'.join(path), 'The min attribute is not of type "int"')
        if min_items is not None and min_items < 0:
            raise SchemaError('.'.join(path), 'The min attribute is not a non-negative integer')
        max_items = None
        if 'max' in component_def:
            max_items = component_def['max']
        if max_items is not None and not isinstance(max_items, int):
            raise SchemaError('.'.join(path), 'The max attribute is not of type "int"')
        if max_items is not None and max_items < 0:
            raise SchemaError('.'.join(path), 'The max attribute is not a non-negative integer')
        if min_items and max_items and min_items > max_items:
            raise SchemaError('.'.join(path), 'The min attribute is greatr than max')
        return ListDescriptor(component_def['item_types'], min_items, max_items,
                              self.descriptors)

    def get_definition(self,
                       component_type: str)\
            -> Optional[Dict[str, Any]]:
        """
        This method finds and returns definition for the specified component type.

        :param component_type: The string representation of a the component's type.
        :return:
        """
        for component_def in self.schema_def['items']:
            if component_type in component_def:
                return component_def[component_type]
        return None

    def validate(self,
                 doc: Descriptor)\
            -> bool:
        """
        This method validates the provided document against the Schema instance's own schema.

        :param doc: The document to be validated.
        :return: True if the document is valid or raises a ValidationError if not.
        """
        return self.schema.validate(doc, [])
