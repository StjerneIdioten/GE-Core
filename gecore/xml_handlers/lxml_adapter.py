import logging
from pathlib import Path
from lxml import etree

from gecore.xml_handlers.xml_interface import XMLInterface


class LXMLAdapter(XMLInterface):
    def __init__(self, filename: Path):
        self.logger = logging.getLogger(__name__)
        try:
            self._tree = etree.parse(str(filename), parser=etree.XMLParser(remove_blank_text=True))
        except (etree.ParseError, FileNotFoundError) as e:
            self.logger.exception(e)

    def getroot(self):
        return self._tree.getroot()

    def Element(self):
        raise NotImplementedError

    def SubElement(self):
        raise NotImplementedError
