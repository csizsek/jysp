"""
This module contains the descriptors, the basic building blocks of the schema. All the descriptors
inherit from an abstract base class called Descriptor and implement the different component type
specific validation logic that is needed for the schema loading and validation.
"""

from abc import ABC
from typing import Dict, List, Optional

from error import ValidationError   # pylint: disable=no-name-in-module


class Descriptor(ABC):  # pylint: disable=too-few-public-methods
    """
    Base class or all the descriptor classes.
    """


class IncompleteTypeDescriptor(Descriptor):
    """
    Descriptor class for incomplete descriptors.
    This descriptor is never valid.
    """

    @staticmethod
    def validate(component: Descriptor,
                 path: List[str])\
            -> bool:
        """
        This validation method always throws a ValidationError because an incomplete descriptor can
        never be valid.

        :param component: The component to be validated.
        :param path: The path of the component to be validated.
        :return: IncompleteTypedescriptors are never valid, calling the validate method will raise
            an exception.
        """
        raise ValidationError('.'.join(path), 'Incomplete component definition')

    def __str__(self) -> str:
        return 'IncompleteTypeDescriptor'


class BoolDescriptor(Descriptor):
    """
    Descriptor for boolean components.
    """
    @staticmethod
    def validate(component: Descriptor,
                 path: List[str])\
            -> bool:
        """
        Validation method that decides whether the provided component is a valid boolean descriptor.

        :param component: The component to be validated.
        :param path: The path of the component to be validated.
        :return: True if the component is valid otherwise the method will throw a ValidationError.
        """
        if component is None or not isinstance(component, bool):
            raise ValidationError('.'.join(path), 'Expected type: bool')
        return True

    def __str__(self) -> str:
        return 'BoolDescriptor'


class StringDescriptor(Descriptor):
    """
    Descriptor for string components.
    """
    @staticmethod
    def validate(component: Descriptor,
                 path: List[str])\
            -> bool:
        """
        Validation method that decides whether the provided component is a valid boolean descriptor.

        :param component: The component to be validated.
        :param path: The path of the component to be validated.
        :return: True if the component is valid otherwise the method will throw a ValidationError.
        """
        if component is None or not isinstance(component, str):
            raise ValidationError('.'.join(path), 'Expected type: string')
        return True

    def __str__(self) -> str:
        return 'StringDescriptor'


class IntDescriptor(Descriptor):
    """
    Descriptor for integer components.
    """
    @staticmethod
    def validate(component: Descriptor,
                 path: List[str])\
            -> bool:
        """
        Validation method that decides whether the provided component is a valid integer descriptor.

        :param component: The component to be validated.
        :param path: The path of the component to be validated.
        :return: True if the component is valid otherwise the method will throw a ValidationError.
        """
        if component is None or not isinstance(component, int):
            raise ValidationError('.'.join(path), 'Expected type: int')
        return True

    def __str__(self) -> str:
        return 'IntDescriptor'


class FloatDescriptor(Descriptor):
    """
    Descriptor for floating point components.
    """
    @staticmethod
    def validate(component: Descriptor,
                 path: List[str])\
            -> bool:
        """
        Validation method that decides whether the provided component is a valid float descriptor.

        :param component: The component to be validated.
        :param path: The path of the component to be validated.
        :return: True if the component is valid otherwise the method will throw a ValidationError.
        """
        if component is None or not isinstance(component, float):
            raise ValidationError('.'.join(path), 'Expected type: float')
        return True

    def __str__(self) -> str:
        return 'FloatDescriptor'


class MapItem:  # pylint: disable=too-few-public-methods
    """
    Item type for the MapDescriptor.
    """
    def __init__(self,
                 name: str,
                 item_type: str,
                 required: bool):
        self.name = name
        self.item_type = item_type
        self.required = required

    def __str__(self) -> str:
        return 'MapItem(name={0},type={1},required={2})'.format(
            self.name, self.item_type, self.required)


class MapDescriptor(Descriptor):
    """
    Descriptor for map type (i.e. collection of key-value pair) components.
    """
    def __init__(self,
                 items: List[MapItem],
                 descriptors: Dict[str, Descriptor]):
        """
        Constructor method for the map descriptor.

        :param items: The item collection of the map.
        :param descriptors: Descriptors for the map items.
        """
        self.items = {item.name: item for item in items}
        self.descriptors = descriptors

    def validate(self,
                 component: Descriptor,
                 path: List[str])\
            -> bool:
        """
        Validation method that decides whether the provided component is a valid map descriptor.

        :param component: The component to be validated.
        :param path: The path of the component to be validated.
        :return: True if the component is valid otherwise the method will throw a ValidationError.
        """
        required_items: Dict[str, bool] = {key: False for key in self.items
                                           if self.items[key].required}
        if component is None:
            if not required_items:
                return True
            raise ValidationError('.'.join(path), 'No components found')

        if not isinstance(component, dict):
            raise ValidationError('.'.join(path), 'Expected type: map')

        for key in component:
            if key not in self.items:
                raise ValidationError('.'.join(path), 'Unexpected item: "{0}"'.format(key))
            path.append(key)
            required_items[key] = self.descriptors[
                self.items[key].item_type].validate(component[key], path)
            path.pop()

        for key in required_items:
            if not required_items[key]:
                raise ValidationError('.'.join(path), 'Missing required item: "{0}"'.format(key))
        return True

    def __str__(self) -> str:
        ret = 'MapDescriptor('
        ret += ','.join([str(self.items[item]) for item in self.items])
        ret += ')'
        return ret


class ListDescriptor(Descriptor):
    """
    Descriptor class for list type components.
    """
    def __init__(self,
                 item_types: List[str],
                 min_items: Optional[int],
                 max_items: Optional[int],
                 descriptors: Dict[str, Descriptor]):
        """
        Constructor method for the map descriptor.

        :param item_types: The item types of the list.
        :param min_items: Number of minimum occurrences.
        :param max_items: Number of maximum occurrences.
        :param descriptors: Descriptors for the list items.
        """
        self.item_types: List[str] = [t for t in item_types]
        self.descriptors: Dict[str, Descriptor] = descriptors
        self.min_items = min_items
        self.max_items = max_items

    def validate(self,
                 component: Descriptor,
                 path: List[str])\
            -> bool:
        """
        Validation method that decides whether the provided component is a valid list descriptor.

        :param component: The component to be validated.
        :param path: The path of the component to be validated.
        :return: True if the component is valid otherwise the method will throw a ValidationError.
        """
        if component is None:
            if not self.min_items:
                return True
            raise ValidationError('.'.join(path), 'Too few list '
                                                  'items: min={0}'.format(self.min_items))
        if not isinstance(component, list):
            raise ValidationError('.'.join(path), 'Expected type: list')
        item_cnt = 0
        for item in component:
            for key in item:
                if key not in self.item_types:
                    raise ValidationError('.'.join(path),
                                          'Unexpected type: "{0}"'.format(key))
                path.append('items[{0}]'.format(item_cnt))
                self.descriptors[key].validate(item[key], path)
                path.pop()
            item_cnt += 1
            if self.max_items and item_cnt > self.max_items:
                raise ValidationError('.'.join(path), 'Too many list '
                                      'items: max={0}'.format(self.max_items))
        if self.min_items and item_cnt < self.min_items:
            raise ValidationError('.'.join(path), 'Too few list '
                                  'items: min={0}'.format(self.min_items))
        return True

    def __str__(self) -> str:
        ret = 'ListDescriptor('
        ret += ','.join(self.item_types)
        ret += ')'
        return ret
