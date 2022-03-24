from abc import (ABC, abstractmethod)
from pathlib import Path
from typing import (Dict, Optional, NewType)

XPath = NewType('XPath', str)


class XMLWriter(ABC):
    @abstractmethod
    def __init__(self, filename: Path, root_name: str, root_attrib: Dict[str, str]):
        raise NotImplementedError

    @abstractmethod
    def write_to_file(self, xml_declaration=True, encoding='iso-8859-1'):
        raise NotImplementedError

    @abstractmethod
    def create_element(self, name: str, xpath_parent: Optional[XPath], attrib: Dict[str, str] = None) -> XPath:
        raise NotImplementedError


class XMLReader(ABC):
    @abstractmethod
    def __init__(self, filepath: Path):
        raise NotImplementedError

    @abstractmethod
    def read_element(self):
        raise NotImplementedError
