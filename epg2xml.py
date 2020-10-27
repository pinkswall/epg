from xml.etree.ElementTree import Element, SubElement, ElementTree, fromstring
from typing import Dict, List, Tuple
import sys
import json

from DumpChannels import *
from GenerateXML import *
from GetEPG import *


config = {
    'fetch_day': 3,
    'path_to_channels': './Channels.json'
}


def addEndTime(EPGs):
    """
    EPG에 방송종료시각(EndTime)을 추가합니다. \n
    방송종료시각은 다음 방송의 방송시작시각입니다. \n
    마지막 방송은 제거됩니다.
    """
    EPGsIter = iter(sorted(EPGs, key=lambda EPG: EPG['StartTime']))
    currentEPG = next(EPGsIter)
    result = []
    for nextEPG in EPGsIter:
        currentEPG['EndTime'] = nextEPG['StartTime']
        result.append(currentEPG)
        currentEPG = nextEPG
    return result
    
def validateChannel(Channel: Dict, DumpedChannels: List):
    """
    잘못된 채널을 필터하고, 부족한 정보가 있으면 덤프에서 추가합니다. \n
    @return UpdatedChannel | None
    """
    for dumpedChannel in DumpedChannels:
        # 'ServiceId' 값이 올바르지 않은 채널 필터
        if Channel['ServiceId'] == dumpedChannel['ServiceId']:
            # 'Id' 값이 없는 채널 필터
            if 'Id' not in Channel: return None
            # 덤프에서 부족한 정보 업데이트
            for keyOfDump in dumpedChannel.keys():
                Channel.setdefault(keyOfDump, dumpedChannel[keyOfDump])
            return Channel     
    return None

def requestEPG(Channel: Dict, period: int, SetDumpedChannels) -> Tuple:
    """
    올바른 ServiceId에 한해, EPG를 요청합니다. \n
    @return (Channel, SetDumpedChannels): Tuple \n
    @return Channel: Dict - 기존 Channel에 덤프에 있던 정보와 EPG 정보가 추가되었습니다. \n
    @return Channel['EPG']: List - EPG 정보. 자세한 값은 GetEPG 함수 참고 \n
    @return SetDumpedChannels: Dict - {'SourceName': Dump}
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
            Channel['EPG'] = addEndTime(GetEPGFromSKB(Channel['ServiceId'], period))      
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
            Channel['EPG'] = addEndTime(GetEPGFromLGU(Channel['ServiceId'], period))
            return (Channel, SetDumpedChannels)
        print('잘못된 ServiceId :', Channel['Name'], ", " , Channel["serviceId"])
        return (None, SetDumpedChannels)


    # NAVER
    if Channel['Source'] == "NAVER":
        if 'NAVER' not in SetDumpedChannels:
            SetDumpedChannels["NAVER"] = DumpChannelsFromNAVER()
        Channel = validateChannel(Channel, SetDumpedChannels['NAVER'])
        if Channel:
            Channel['EPG'] = addEndTime(GetEPGFromNAVER(Channel['ServiceId'], period))
            return (Channel, SetDumpedChannels)
        print('잘못된 ServiceId :', Channel['Name'], ", " , Channel["serviceId"])
        return (None, SetDumpedChannels)
    

    # TVING
    if Channel['Source'] == "TVING":
        if 'TVING' not in SetDumpedChannels:
            SetDumpedChannels["TVING"] = DumpChannelsFromTVING()
        Channel = validateChannel(Channel, SetDumpedChannels['TVING'])
        if Channel:
            Channel['EPG'] = addEndTime(GetEPGFromTVING(Channel['ServiceId'], period))
            return (Channel, SetDumpedChannels)
        print('잘못된 ServiceId :', Channel['Name'], ", " , Channel["serviceId"])
        return (None, SetDumpedChannels)


    # WAVVE
    if Channel['Source'] == "WAVVE":
        if 'WAVVE' not in SetDumpedChannels:
            SetDumpedChannels["WAVVE"] = DumpChannelsFromWAVVE()
        Channel = validateChannel(Channel, SetDumpedChannels['WAVVE'])
        if Channel:
            Channel['EPG'] = addEndTime(GetEPGFromWAVVE(Channel['ServiceId'], period))
            return (Channel, SetDumpedChannels)
        print('잘못된 ServiceId :', Channel['Name'], ", " , Channel["serviceId"])
        return (None, SetDumpedChannels)


# channels.json 읽기
try:
    with open(config['path_to_channels'], 'r', encoding='UTF-8') as file_json:
        Channels = json.load(file_json)
except Exception as e:
    print('채널 파일을 읽는 중 에러가 발생했습니다.')
    print(str(e))

SetDumpedChannels = None
XmlChannels = []
XmlPrograms = []

# EPG2XML:STR
for Channel in Channels:
    # UpdatedChannel은 결여된 정보와 EPG가 추가된 Channel임.
    UpdatedChannel, SetDumpedChannels = requestEPG(Channel=Channel, period=config['fetch_day'], SetDumpedChannels=SetDumpedChannels)
    if UpdatedChannel is not None:
        XmlChannels.append(writeChannel(channelInfo=Channel))
        for Program in UpdatedChannel['EPG']:
            if Program['Title'] is None: continue
            XmlPrograms.append(writeProgram(Program, UpdatedChannel['Id']))

# TODO: Dump Write
tv = Element('tv', attrib={'generator-info-name': 'pink-epg 0.0.1'})
for XmlChannel in XmlChannels:
    tv.append(fromstring(XmlChannel))
for XmlProgram in XmlPrograms:
    tv.append(fromstring(XmlProgram))

ElementTree(tv).write("xmltv.xml", encoding="UTF-8", xml_declaration=True)