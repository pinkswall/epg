from xml.etree.ElementTree import Element, SubElement, ElementTree, tostring
from typing import Dict

def writeProgram(programInfo: Dict) -> str:
    """
    프로그램 정보를 입력받아 xml형식으로 정리합니다. \n
    @param programInfo - \n
    {
        'id': '채널ID',
        'title': '제목',
        'subtitle': '부제목' | None,
        'icon': 'https://ddns/path/to/icon' | None,
        'description': '~~하고 ~~하는 프로그램' | None,
        'category': '카테고리',
        'credits': [ { 'name': '이름', 'type': '직종', 'role': '역할' | None } ] | None,
        'startTime': 'YYYYMMDDhhmmss +0900',
        'endTime': 'YYYYMMDDhhmmss +0900',
        'episode': 'n회' | None,
        'isRebroadcast': True | False,
        'KMRB': '전체관람가' | '12세이상관람가' | '15세이상관람가' | '청소년관람불가' | None
    } \n
    @return xml string
    """

    program = Element('programme', start=programInfo['startTime'], stop=programInfo['endTime'], channel=programInfo['id'])

    SubElement(program, 'title', attrib={'lang': 'kr'}).text = programInfo['title']

    if programInfo['icon']: SubElement(program, 'icon', attrib={'src': programInfo['icon']})

    if programInfo['subtitle']:  SubElement(program, 'sub-title', attrib={'lang': "kr"}).text = programInfo['subtitle']

    if programInfo['description']: SubElement(program, 'desc', attrib={'lang': 'kr'}).text = programInfo['description']

    if programInfo['credits']:
        ElemCredits = SubElement(program, 'credits')
        for credit in programInfo['credits']:
            if credit['role']:
                SubElement(ElemCredits, credit['type'], attrib={'role': credit['role']}).text = credit['name']
            else:
                SubElement(ElemCredits, credit['type']).text = credit['name']

    SubElement(program, 'category', attrib={'lang': 'kr'}).text = programInfo['category']

    if programInfo['episode']: SubElement(program, 'episode-num', attrib={'system': 'onscreen'})

    if programInfo['isRebroadcast']: SubElement(program, 'previously-shown')

    if programInfo['KMRB']:
        SubElement(SubElement(program, 'rating', attrib={'system': 'KMRB'}), 'value').text = programInfo['KMRB']


    return tostring(program, encoding='unicode')