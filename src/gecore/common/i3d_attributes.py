from __future__ import annotations
from abc import (ABC, abstractmethod)
from typing import (Any, Union, Dict, List)


AttributeValue = Any[bool, int, float, List[float], str]


class Attribute(ABC):
    def __init__(self,
                 name: str,
                 value_default: AttributeValue,
                 value: AttributeValue,
                 name_displayed: str,
                 dependencies: List[IAttributeDependency]):
        self.name: str = name
        self.value_default: AttributeValue = value_default
        self.value: AttributeValue = value
        self.name_displayed: str = name_displayed
        self.dependencies: List[IAttributeDependency] = dependencies


class Number(Attribute):
    pass


class Enum(Attribute):
    pass


class IAttributeDependency(ABC):
    def __init__(self, attribute: Attribute):
        self.attribute: Attribute = 0

    @abstractmethod
    def dependency_fulfilled(self) -> bool:
        return NotImplementedError


class DiscreteDependency(IAttributeDependency):
    def __init__(self, value: Attribute, values_allowed: List[AttributeValue]):
        self.values_allowed: List[AttributeValue] = values_allowed
        super().__init__(value)

    def dependency_fulfilled(self) -> bool:
        return self.attribute.value in self.values_allowed


class AttributeGroup:
    def __init__(self):
        self.attributes: List[Attribute] = []

    def add_attribute(self, attribute: Attribute):
        self.attributes.append(attribute)


class AttributeStandard:
    pass
