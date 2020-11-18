from xml.etree.ElementTree import Element, SubElement, tostring
from typing import Optional, TypedDict

class Channel(TypedDict):
    Id: Optional[str]
    Name: str
    Icon_url: Optional[str]

def writeChannel(channelInfo: Channel) -> str:
    """
    채널 정보를 입력받아 xml형식으로 정리합니다. \n
    :param channelInfo: Channel \n
    :return: xml string 
    """
    
    if 'Id' not in channelInfo:
        channelInfo['Id'] = channelInfo['Name']
        
    channel = Element('channel', id=channelInfo['Id'])

    SubElement(channel, 'display-name').text = channelInfo['Name']

    if 'Icon_url' in channelInfo: SubElement(channel, 'icon', attrib={'src': channelInfo['Icon_url']})

    return tostring(channel, encoding='unicode')