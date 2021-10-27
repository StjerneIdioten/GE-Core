from abc import (ABC, abstractmethod)
from pathlib import Path
from typing import (Dict, Optional, NewType)

XPath = NewType('XPath', str)


class XMLWriter(ABC):
    @abstractmethod
    def __init__(self, filename: Path, root_name: str, root_attrib: Dict[str, str]):
        raise NotImplementedError

    @abstractmethod
    def select_element(self, element: XPath):
        raise NotImplementedError

    @abstractmethod
    def write_to_file(self, xml_declaration=True, encoding='iso-8859-1'):
        raise NotImplementedError

    @abstractmethod
    def create_element(self, name: str, parent: Optional[XPath], attrib: Dict[str, str] = None):
        raise NotImplementedError

    @abstractmethod
    def sub_element(self, name: str, attrib: Dict[str, str] = None):
        raise NotImplementedError


class XMLReader(ABC):
    @abstractmethod
    def __init__(self, filepath: Path):
        raise NotImplementedError

    @abstractmethod
    def read_element(self):
        raise NotImplementedError
