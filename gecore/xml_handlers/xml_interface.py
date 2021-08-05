from abc import (ABC, abstractmethod)
from pathlib import Path
import logging


class XMLInterface(ABC):
    @abstractmethod
    def __init__(self, filepath: Path):
        raise NotImplementedError

    @abstractmethod
    def getroot(self):
        raise NotImplementedError

    @abstractmethod
    def Element(self):
        raise NotImplementedError

    @abstractmethod
    def SubElement(self):
        raise NotImplementedError
