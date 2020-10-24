from xml.etree.ElementTree import Element, SubElement, ElementTree, tostring
from typing import Dict

def writeChannel(channelInfo: Dict):
    """
    채널 정보를 입력받아 xml형식으로 정리합니다. \n
    @param channelInfo - \n
    {
        'id': '채널ID',
        'name': '채널이름',
        'icon': 'https://ddns/path/to/icon'
    } \n
    @return xml string
    """

    channel = Element('channel', id=channelInfo['id'])

    SubElement(channel, 'display-name').text = channelInfo['name']

    SubElement(channel, 'icon', attrib={'src': channelInfo['icon']})

    return tostring(channel, encoding='unicode')