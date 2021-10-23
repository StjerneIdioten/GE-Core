import logging
from pathlib import Path
from lxml import etree
from typing import Dict

from gecore.xml_handlers import (XMLWriter, XMLReader)


class LXMLReader(XMLReader):
    def __init__(self, filename: Path):
        self.log = logging.getLogger(__name__)
        try:
            self._tree = etree.parse(str(filename), parser=etree.XMLParser(remove_blank_text=True))
        except (etree.ParseError, FileNotFoundError) as e:
            self.log.exception(e)
            raise

    def read_element(self):
        raise NotImplementedError


def resolve_namespacing_of_attributes(attrib: Dict[str, str]):
    resolved = {'attrib': {}, 'nsmap': {}}
    namespaced = []
    for key, value in attrib.items():
        if ':' in key:
            split_key = key.split(':')
            if split_key[0] == 'xmlns':
                resolved['nsmap'][split_key[1]] = value
            else:
                namespaced.append((*split_key, value))
        else:
            resolved['attrib'][key] = value

    for attribute in namespaced:
        resolved['attrib'][etree.QName(resolved['nsmap'][attribute[0]], attribute[1])] = attribute[2]

    return resolved


class LXMLWriter(XMLWriter):
    def __init__(self, file: Path, root_name: str, root_attrib: Dict[str, str]):
        self.log = logging.getLogger(__name__)
        self._file= file
        self._root = etree.Element(root_name, **resolve_namespacing_of_attributes(root_attrib))
        self._current_element = self._root

    def write_to_file(self, settings=None):
        settings = {'xml_declaration': True,
                    'encoding': 'iso-8859-1',
                    'method': 'xml',
                    'pretty_print': True
                    } if settings is None else settings

        with self._file.open('w') as f:
            tree_string = etree.tostring(etree.ElementTree(self._root), **settings).decode(settings['encoding'])
            tree_string = tree_string.replace("&gt;", ">")
            f.write(tree_string)

    def create_element(self, name: str, parent=None, attrib: Dict[str, str] = None):
        etree.SubElement(self._current_element, name, **resolve_namespacing_of_attributes(attrib))
