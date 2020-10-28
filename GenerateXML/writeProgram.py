from xml.etree.ElementTree import Element, SubElement, tostring
from typing import Dict

def writeProgram(programInfo: Dict, Id: str) -> str:
    """
    프로그램 정보를 입력받아 xml형식으로 정리합니다. \n
    @param programInfo - \n
    {
        'Title': '제목',
        'Subtitle'?: '부제목',
        'Icon_url'?: 'https://ddns/path/to/icon',
        'Episode'?: 'n회',
        'Description'?: '~~하고 ~~하는 프로그램',
        'Category'?: '카테고리',
        'Credits'?: [ { 'Name': '이름', 'Type': '직종', 'Role'?: '역할' } ],
        'StartTime': 'YYYYMMDDhhmmss +0900',
        'EndTime': 'YYYYMMDDhhmmss +0900',
        'IsRebroadcast'?: True | False,
        'KCSC'?: '모든연령시청가' | '7세이상시청가' | '12세이상시청가' | '15세이상시청가' | '19세이상시청가'
    } \n
    @return xml string
    """

    program = Element('programme', start=programInfo['StartTime'], stop=programInfo['EndTime'], channel=Id)

    SubElement(program, 'title', attrib={'lang': 'kr'}).text = programInfo['Title']

    if ('Icon_url' in programInfo) and programInfo['Icon_url']: SubElement(program, 'icon', attrib={'src': programInfo['Icon_url']})

    if ('Subtitle' in programInfo) and programInfo['Subtitle']: SubElement(program, 'sub-title', attrib={'lang': "kr"}).text = programInfo['Subtitle']

    if ('Description' in programInfo) and programInfo['Description']: SubElement(program, 'desc', attrib={'lang': 'kr'}).text = programInfo['Description']

    if ('Credits' in programInfo) and programInfo['Credits']:
        ElemCredits = SubElement(program, 'credits')
        for credit in programInfo['Credits']:
            if ('Role' in credit) and programInfo['Role']:
                SubElement(ElemCredits, credit['Type'], attrib={'role': credit['Role']}).text = credit['Name']
            else:
                SubElement(ElemCredits, credit['Type']).text = credit['Name']

    if ('Category' in programInfo) and programInfo['Category']: SubElement(program, 'category', attrib={'lang': 'kr'}).text = programInfo['Category']

    if ('Episode' in programInfo) and programInfo['Episode']: SubElement(program, 'episode-num', attrib={'system': 'onscreen'}).text = programInfo['Episode']

    if ('IsRebroadcast' in programInfo) and programInfo['IsRebroadcast']: SubElement(program, 'previously-shown')

    if ('KCSC' in programInfo) and programInfo['KCSC']: SubElement(SubElement(program, 'rating', attrib={'system': 'KCSC'}), 'value').text = programInfo['KCSC']


    return tostring(program, encoding='unicode')