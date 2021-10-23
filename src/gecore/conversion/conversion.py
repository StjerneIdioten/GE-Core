import logging
logger = logging.getLogger(__name__)

from gecore.conversion.source import Source
from gecore.conversion.destination import Destination


class Converter:
    def __init__(self, source: Source, destination: Destination):
        self.source: Source = source
        self.destination: Destination = destination


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Converter to/from I3D")
    # add argument
    parser.add_argument('-s', '--sourceType', nargs=1, metavar='sourceType',
                        help="Type of source to use")
    parser.add_argument('source', nargs=1, metavar='source', help='Path to source')
    parser.add_argument('-d', '--destinationType', nargs=1, metavar='destinationType',
                        help="Type of destination to use")
    parser.add_argument('destination', nargs=1, metavar='destination', help='Path to destination')
    args = parser.parse_args()
