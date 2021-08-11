import logging
from pathlib import Path
import xml.etree.ElementTree as ET

from gecore.xml_handlers.xml_interface import XMLInterface


class EtreeAdapter(XMLInterface):
    def __init__(self, filename: Path):
        self.logger = logging.getLogger(__name__)
        try:
            self._tree = ET.parse(str(filename), parser=ET.XMLParser(target=CommentedTreeBuilder()))
        except (ET.ParseError, FileNotFoundError) as e:
            self.logger.exception(e)

    def getroot(self):
        return self._tree.getroot()

    def Element(self):
        raise NotImplementedError

    def SubElement(self):
        raise NotImplementedError


class CommentedTreeBuilder(ET.TreeBuilder):
    """
    This class is used to enable elemtree to NOT delete comments of parsed trees...
    https://stackoverflow.com/a/34324359
    """
    def comment(self, data):
        self.start(ET.Comment, {})
        self.data(data)
        self.end(ET.Comment)
