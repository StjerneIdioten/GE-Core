import pytest
import xml.etree.ElementTree as ET
from pathlib import Path
from gecore.xml_handlers import EtreeWriter


class TestXmlWriters:
    def test_basic_write_to_file(self, tmp_path):
        # Populate with test data and write
        test_xml_root_attributes = {'testField': 'TestValue',
                           'testns:test1': 'data',
                           'xmlns:testns': 'http://test.test/testnamespace.xsd'
                           }
        test_file = tmp_path / 'basic_write_to_file.xml'
        test_root_name = 'TestRoot'
        xml_writer = EtreeWriter(test_file, test_root_name, test_xml_root_attributes)

        settings = {
            'xml_declaration': True,
            'encoding': 'iso-8859-1',
            'method': 'xml'
        }

        xml_writer.write_to_file(settings)

        # Test document xml declaration
        with open(test_file, 'r') as f:
            assert f.readline().rstrip('\n\r') == "<?xml version='1.0' encoding='iso-8859-1'?>"

        # Test root element
        tree = ET.parse(str(test_file))
        root = tree.getroot()
        assert root.tag == test_root_name
        assert root.attrib['testField'] == 'TestValue'
        assert root.attrib['{http://test.test/testnamespace.xsd}test1'] == 'data'

    def test_create_element(self, tmp_path):
        root_name = 'CreateElement'
        xml_writer = EtreeWriter(tmp_path / 'create_element.xml', root_name)

        element_parent_tag = 'elementParent'
        element_parent_xpath = xml_writer.create_element(tag=element_parent_tag)
        assert element_parent_xpath == f"./{element_parent_tag}[1]"

        element_child_tag = 'elementChild'
        element_child_xpath = xml_writer.create_element(tag=element_child_tag, xpath_parent=element_parent_xpath)
        assert element_child_xpath == f"{element_parent_xpath}/{element_child_tag}[1]"

        for i in range(2, 5):
            assert xml_writer.create_element(tag=element_child_tag, xpath_parent=element_parent_xpath) == \
                   f"{element_parent_xpath}/{element_child_tag}[{i}]"
