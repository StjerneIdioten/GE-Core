from abc import (ABC, abstractmethod)
from pathlib import Path
from typing import Dict


class XMLWriter(ABC):
    @abstractmethod
    def __init__(self, filename: Path, root_name: str, root_attrib: Dict[str, str]):
        raise NotImplementedError

    @abstractmethod
    def write_to_file(self, settings={}):
        raise NotImplementedError

    @abstractmethod
    def create_element(self, name: str, parent=None, attrib: Dict[str, str] = None):
        raise NotImplementedError


class XMLReader(ABC):
    @abstractmethod
    def __init__(self, filepath: Path):
        raise NotImplementedError

    @abstractmethod
    def read_element(self):
        raise NotImplementedError
