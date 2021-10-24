import pytest
import xml.etree.ElementTree as ET
from pathlib import Path
from gecore.xml_handlers import EtreeWriter


class TestXmlWriters:
    def test_basic_write_to_file(self, tmp_path):
        # Populate with test data and write
        test_xml_root_attributes = {'name': 'TestName',
                           'testns:test1': 'data',
                           'xmlns:testns': 'http://test.test/testnamespace.xsd'
                           }
        test_file = tmp_path / 'basic_write.xml'
        print(test_file)
        test_element_name = 'TestElement'
        xml_writer = EtreeWriter(test_file, test_element_name, test_xml_root_attributes)

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
        assert root.tag == test_element_name
        assert root.attrib['name'] == 'TestName'
        assert root.attrib['{http://test.test/testnamespace.xsd}test1'] == 'data'
