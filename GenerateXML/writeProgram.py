from xml.etree.ElementTree import Element, SubElement, ElementTree, tostring
from typing import Dict

def writeProgram(programInfo: Dict):
    """
    프로그램 정보를 입력받아 xml형식으로 정리합니다. \n
    @param {
        'programTitle': '제목',
        'subtitle': '부제목' | None,
        'category': '카테고리',
        'startTime': 'YYYYMMDDhhmmss',
        'episode': 'n회' | None,
        'isRebroadcast': True | False,
        'KMRB': '전체관람가' | '12세이상관람가' | '15세이상관람가' | '청소년관람불가' | None
    } \n
    @return xml string
    """
