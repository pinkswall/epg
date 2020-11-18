from xml.etree.ElementTree import Element, SubElement, tostring
from typing import Optional, TypedDict, Literal


class Credit(TypedDict):
    Name: str
    Type: str
    Role: Optional[str]

class Program(TypedDict):
    Title: str
    Subtitle: Optional[str]
    Icon_url: Optional[str]
    Episode: Optional[str]
    Description: Optional[str]
    Category: Optional[str]
    Credits: Optional[Credit]
    StartTime: str
    EndTime: str
    IsRebroadcast: bool
    KCSC: Optional[Literal['모든연령시청가', '7세이상시청가', '12세이상시청가', '15세이상시청가', '19세이상시청가']]


def writeProgram(programInfo: Program, Id: str) -> str:
    """
    프로그램 정보를 입력받아 xmltv형식으로 정리합니다.

    :param programInfo: Program \n
    :param Id: str \n
    :return: xml string
    """

    program = Element('programme', start=programInfo['StartTime'], stop=programInfo['EndTime'], channel=Id)

    SubElement(program, 'title', attrib={'lang': 'kr'}).text = programInfo['Title']

    if 'Icon_url' in programInfo: SubElement(program, 'icon', attrib={'src': programInfo['Icon_url']})

    if 'Subtitle' in programInfo: SubElement(program, 'sub-title', attrib={'lang': "kr"}).text = programInfo['Subtitle']

    if 'Description' in programInfo: SubElement(program, 'desc', attrib={'lang': 'kr'}).text = programInfo['Description']

    if 'Credits' in programInfo:
        ElemCredits = SubElement(program, 'credits')
        for credit in programInfo['Credits']:
            if 'Role' in credit:
                SubElement(ElemCredits, credit['Type'], attrib={'role': credit['Role']}).text = credit['Name']
            else:
                SubElement(ElemCredits, credit['Type']).text = credit['Name']

    if 'Category' in programInfo: SubElement(program, 'category', attrib={'lang': 'kr'}).text = programInfo['Category']

    if 'Episode' in programInfo: SubElement(program, 'episode-num', attrib={'system': 'onscreen'}).text = programInfo['Episode']

    if programInfo['IsRebroadcast']: SubElement(program, 'previously-shown')

    if 'KCSC' in programInfo: SubElement(SubElement(program, 'rating', attrib={'system': 'KCSC'}), 'value').text = programInfo['KCSC']


    return tostring(program, encoding='unicode')