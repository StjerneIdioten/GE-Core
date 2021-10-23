import pytest
from lxml import etree
from pathlib import Path
from gecore.xml_handlers import LXMLWriter


class TestXmlWriters:
    def test_basic_write_to_file(self, tmp_path):
        # Populate with test data and write
        test_xml_root_attributes = {'name': 'TestName',
                           'testns:test1': 'data',
                           'xmlns:testns': 'http://test.test/testnamespace.xsd'
                           }
        test_file = tmp_path / 'basic_write.xml'
        test_element_name = 'TestElement'
        xml_writer = LXMLWriter(test_file, test_element_name, test_xml_root_attributes)

        settings = {
            'xml_declaration': True,
            'encoding': 'iso-8859-1',
            'method': 'xml',
            'pretty_print': True
        }

        xml_writer.write_to_file(settings)

        # Read result using lxml
        tree = etree.parse(str(test_file))

        # Test document info
        assert tree.docinfo.xml_version == '1.0'
        assert tree.docinfo.encoding == 'iso-8859-1'

        # Test root element
        root = tree.getroot()
        assert root.tag == test_element_name
        assert root.attrib['name'] == 'TestName'
        assert root.attrib['{http://test.test/testnamespace.xsd}test1'] == 'data'
