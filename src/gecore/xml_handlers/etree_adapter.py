import logging
from pathlib import Path
import xml.etree.ElementTree as ET
from typing import (Dict, Optional)

from gecore.xml_handlers import (XMLWriter, XMLReader, XPath)


class EtreeWriter(XMLWriter):
    def __init__(self, file: Path, root_name: str = 'root', root_attrib: Dict[str, str] = None):
        self.log = logging.getLogger(__name__)
        self._file = file
        self._root = ET.Element(root_name, root_attrib or {})
        self._current_element = None

    def write_to_file(self, xml_declaration=True, encoding='iso-8859-1'):
        tree = ET.ElementTree(self._root)
        ET.indent(tree)
        tree.write(self._file, xml_declaration=xml_declaration, encoding=encoding, method='xml')

    def create_element(self, tag: str, xpath_parent=None, attrib: Dict[str, str] = None) -> XPath:
        if xpath_parent is None:
            parent_element = self._root
            xpath_parent = f"."
        else:
            parent_element = self._root.find(xpath_parent)
            if parent_element is None:
                raise ValueError("The given parent xpath does not resolve to an element")

        # This checks if there are already multiple children with the same tag and assigns the proper index to the xpath
        # for the new element
        path_to_element = f"{xpath_parent}/{tag}[{len(parent_element.findall(f'./{tag}'))+1}]"

        ET.SubElement(parent_element, tag, attrib or {})
        return path_to_element


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