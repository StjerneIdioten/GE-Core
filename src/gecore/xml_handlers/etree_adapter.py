import logging
from pathlib import Path
import xml.etree.ElementTree as ET
from typing import Dict

from gecore.xml_handlers import (XMLWriter, XMLReader, XPath)


class EtreeWriter(XMLWriter):
    def __init__(self, file: Path, root_name: str, root_attrib: Dict[str, str]):
        self.log = logging.getLogger(__name__)
        self._file = file
        self._root = ET.Element(root_name, root_attrib)
        self._current_element = None

    def write_to_file(self, xml_declaration=True, encoding='iso-8859-1'):
        tree = ET.ElementTree(self._root)
        ET.indent(tree)
        tree.write(self._file, xml_declaration=xml_declaration, encoding=encoding, method='xml')

    def select_element(self, element: XPath):
        pass

    def create_element(self, name: str, parent=None, attrib: Dict[str, str] = None):
        if parent is None:
            pass

    def sub_element(self, name: str, attrib: Dict[str, str] = None):
        self._current_element = ET.SubElement(self._current_element, name, attrib)


class EtreeReader(XMLReader):
    pass


class CommentedTreeBuilder(ET.TreeBuilder):
    """
    This class is used to enable elemtree to NOT delete comments of parsed trees...
    https://stackoverflow.com/a/34324359
    """
    def comment(self, data):
        self.start(ET.Comment, {})
        self.data(data)
        self.end(ET.Comment)


# Add support for not escaping certain characters by monkey patching it
def escape_attrib_element_tree(text):
    # escape attribute value
    try:
        if "&" in text:
            text = text.replace("&", "&amp;")
        if "<" in text:
            text = text.replace("<", "&lt;")
        if ">" in text:
            # Needed for the i3d format
            pass
            #text = text.replace(">", "&gt;")
        if "\"" in text:
            text = text.replace("\"", "&quot;")
        # The following business with carriage returns is to satisfy
        # Section 2.11 of the XML specification, stating that
        # CR or CR LN should be replaced with just LN
        # http://www.w3.org/TR/REC-xml/#sec-line-ends
        if "\r\n" in text:
            text = text.replace("\r\n", "\n")
        if "\r" in text:
            text = text.replace("\r", "\n")
        #The following four lines are issue 17582
        if "\n" in text:
            text = text.replace("\n", "&#10;")
        if "\t" in text:
            text = text.replace("\t", "&#09;")
        return text
    except (TypeError, AttributeError):
        ET._raise_serialization_error(text)


# Assign the escape attribute function to replace the default implementation
ET._escape_attrib = escape_attrib_element_tree