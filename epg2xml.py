# https://docs.python.org/ko/3/library/xml.etree.elementtree.html
# http://wiki.xmltv.org/index.php/XMLTVFormat
from xml.etree.ElementTree import Element, SubElement, ElementTree, fromstring, canonicalize
from typing import Dict, List, Tuple
import sys
import json

from DumpChannels import *
from GetEPG import *


config = {
    'fetch_days': 3,
    'path_to_channels': 'Channels.json'
}


# channels.json 읽기
try:
    with open(config['path_to_channels'], 'r', encoding='UTF-8') as file_json:
        Channels = json.load(file_json)
except Exception as e:
    print('채널 파일을 읽는 중 에러가 발생했습니다.')
    print(str(e))


SetDumpedChannels = None
UpdatedChannels = []
for Channel in Channels:
    UpdatedChannel, SetDumpedChannels = requestEPG(Channel, SetDumpedChannels if SetDumpedChannels else None)
    UpdatedChannels.append(UpdatedChannel)
    # TODO


def validateChannel(Channel: Dict, DumpedChannels: List):
    """
    잘못된 ServiceId를 필터하고, 부족한 정보가 있으면 덤프에서 추가합니다. \n
    @return True | False
    """
    for dumpedChannel in DumpedChannels:
        if Channel['ServiceId'] == dumpedChannel['ServiceId']:
            for keyOfDump in dumpedChannel.keys():
                Channel.setdefault(keyOfDump, dumpedChannel[keyOfDump])
            return Channel     
    return None

def requestEPG(Channel: Dict, period: int, SetDumpedChannels: Dict | None) -> Tuple:
    """
    올바른 ServiceId에 한해, EPG를 요청합니다. \n
    @return (Channel, SetDumpedChannels): Tuple \n
    @return Channel: Dict - 기존 Channel에 덤프에만 있던 정보와 EPG 정보가 담겼습니다.
    @return SetDumpedChannels: Dict - 각 소스의 덤프가 담겼습니다.
    """

    if SetDumpedChannels is None:
        SetDumpedChannels = {}

    # SKB
    if Channel['Source'] == "SKB":
        # 덤프가 없으면 요청
        if 'SKB' not in SetDumpedChannels:
            SetDumpedChannels['SKB'] = DumpChannelsFromSKB()

        # Channel ServiceId 검증, Dump에서 부족한 정보 추가 
        Channel = validateChannel(Channel, SetDumpedChannels['SKB'])

        # ServiceId가 올바르면, EPG 요청 후 Channel['EPG']에 저장
        if Channel:
            Channel['EPG'] = GetEPGFromSKB(Channel['ServiceId'], period)
            return (Channel, SetDumpedChannels)
        
        # ServiceId가 올바르지 않으면, 채널 정보 프린트
        print('잘못된 ServiceId :', Channel['Name'], ", " , Channel["serviceId"])
        return (None, SetDumpedChannels)
        

    # LGU
    if Channel['Source'] == "LGU":
        if 'LGU' not in SetDumpedChannels:
            SetDumpedChannels["LGU"] = DumpChannelsFromLGU()
        Channel = validateChannel(Channel, SetDumpedChannels['LGU'])
        if Channel:
            Channel['EPG'] = GetEPGFromLGU(Channel['ServiceId'], period)
            return (Channel, SetDumpedChannels)
        print('잘못된 ServiceId :', Channel['Name'], ", " , Channel["serviceId"])
        return (None, SetDumpedChannels)


    # NAVER
    if Channel['Source'] == "NAVER":
        if 'NAVER' not in SetDumpedChannels:
            SetDumpedChannels["NAVER"] = DumpChannelsFromNAVER()
        Channel = validateChannel(Channel, SetDumpedChannels['NAVER'])
        if Channel:
            Channel['EPG'] = GetEPGFromNAVER(Channel['ServiceId'], period)
            return (Channel, SetDumpedChannels)
        print('잘못된 ServiceId :', Channel['Name'], ", " , Channel["serviceId"])
        return (None, SetDumpedChannels)
    

    # TVING
    if Channel['Source'] == "TVING":
        if 'TVING' not in SetDumpedChannels:
            SetDumpedChannels["TVING"] = DumpChannelsFromTVING()
        Channel = validateChannel(Channel, SetDumpedChannels['TVING'])
        if Channel:
            Channel['EPG'] = GetEPGFromTVING(Channel['ServiceId'], period)
            return (Channel, SetDumpedChannels)
        print('잘못된 ServiceId :', Channel['Name'], ", " , Channel["serviceId"])
        return (None, SetDumpedChannels)


    # WAVVE
    if Channel['Source'] == "WAVVE":
        if 'WAVVE' not in SetDumpedChannels:
            SetDumpedChannels["WAVVE"] = DumpChannelsFromWAVVE()
        Channel = validateChannel(Channel, SetDumpedChannels['WAVVE'])
        if Channel:
            Channel['EPG'] = GetEPGFromWAVVE(Channel['ServiceId'], period)
            return (Channel, SetDumpedChannels)
        print('잘못된 ServiceId :', Channel['Name'], ", " , Channel["serviceId"])
        return (None, SetDumpedChannels)
