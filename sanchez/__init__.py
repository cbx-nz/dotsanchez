# .sanchez file format - Interdimensional Cable Video Format
# Rick & Morty inspired custom video format

__version__ = "1.0.0"
__author__ = "cbx"

from .format import SanchezFile, SanchezMetadata, SanchezConfig
from .encoder import SanchezEncoder
from .decoder import SanchezDecoder
from .player import SanchezPlayer
