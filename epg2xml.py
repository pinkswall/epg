# https://docs.python.org/ko/3/library/xml.etree.elementtree.html
# http://wiki.xmltv.org/index.php/XMLTVFormat
from xml.etree.ElementTree import Element, SubElement, ElementTree, fromstring, canonicalize
from typing import Dict, List, NewType, Callable, Optional

from DumpChannels import *
from GetEPG import *


config = {
    'fetch_days': 3,
}


def epg2xml() -> str:
    # TODO: 덤프뜨고
    # TODO: 덤프 write
    # TODO: channels.json 읽고
    # TODO: 덤프로 validate
    # TODO: valid한 channel만 epg요청
    # TODO:
    # 며칠을 받을건지, serviceId
    return "TO IMPLEMENT"
