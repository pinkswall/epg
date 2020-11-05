from xml.etree.ElementTree import Element, SubElement, tostring
from typing import Dict

def writeChannel(channelInfo: Dict) -> str:
    """
    채널 정보를 입력받아 xml형식으로 정리합니다. \n
    @param channelInfo - \n
    {
        'Id'?: '채널ID',
        'Name': '채널이름',
        'Icon_url'?: 'https://ddns/path/to/icon'
    } \n
    @return xml string
    """
    
    if 'Id' not in channelInfo:
        channelInfo['Id'] = channelInfo['Name']
        
    channel = Element('channel', id=channelInfo['Id'])

    SubElement(channel, 'display-name').text = channelInfo['Name']

    if 'Icon_url' in channelInfo: SubElement(channel, 'icon', attrib={'src': channelInfo['Icon_url']})

    return tostring(channel, encoding='unicode')