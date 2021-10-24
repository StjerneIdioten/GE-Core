import pytest
from pathlib import Path
from gecore.xml_handlers import EtreeReader

pytest.skip("Not Implemented Yet", allow_module_level=True)


# Enables all xml readers to be tested at once with the same tests, by adding them to the list
@pytest.fixture(params=[EtreeReader], scope="module")
def reader_implementation(request):
    return request.param


@pytest.fixture(autouse=True, scope='class')
def reader(request, reader_implementation, resource_path_root):
    request.cls.reader = reader_implementation(resource_path_root / 'xml' / 'reading_test.xml')


class TestXmlReaders:

    def test_read_file(self):
        pass

    def test_read_element(self):
        pass
