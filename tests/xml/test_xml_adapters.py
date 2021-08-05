import pytest
from pathlib import Path
from gecore.xml_handlers.lxml_adapter import LXMLAdapter
from gecore.xml_handlers.elemtree_adapter import EtreeAdapter


@pytest.fixture(params=[LXMLAdapter, EtreeAdapter], scope="module")
def adapter_implementation(request):
    return request.param


@pytest.fixture(autouse=True, scope='class')
def adapter(request, adapter_implementation):
    request.cls.adapter = adapter_implementation(Path(r'test.xml'))


class TestXmlAdapters:

    def test_get_root(self):
        assert self.adapter.getroot().tag == "root"
