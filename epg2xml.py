from xml.etree.ElementTree import Element, SubElement, ElementTree, fromstring
from datetime import datetime, timedelta, date
from typing import Dict, List, Tuple
import os
import sys
import json
import logging

from DumpChannels.FromSKB import DumpChannelsFromSKB
from DumpChannels.FromLGU import DumpChannelsFromLGU
from DumpChannels.FromNAVER import DumpChannelsFromNAVER
from DumpChannels.FromTVING import DumpChannelsFromTVING
from DumpChannels.FromWAVVE import DumpChannelsFromWAVVE

from GetEPG.FromDesktopNAVER import GetEPGFromDesktopNAVER
from GetEPG.FromNAVER import GetEPGFromNAVER
from GetEPG.FromSKB import GetEPGFromSKB
from GetEPG.FromLGU import GetEPGFromLGU
from GetEPG.FromTVING import GetEPGFromTVING
from GetEPG.FromWAVVE import GetEPGFromWAVVE

from GenerateXML.writeChannel import writeChannel
from GenerateXML.writeProgram import writeProgram

config = {
    'fetch_period': 2,
    'path_to_channels': './Channels.json',
    'path_to_dumps_dir': './Dumps',
    'NAVER_more_info': True
}

DIR = os.path.dirname(os.path.abspath(__file__))


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
    잘못된 채널을 걸러내고, 부족한 정보가 있으면 덤프에서 추가합니다. \n
    @return UpdatedChannel | None
    """
    for dumpedChannel in DumpedChannels:
        # 'ServiceId' 값이 올바르지 않은 채널 필터
        if Channel['ServiceId'] == dumpedChannel['ServiceId']:
            # 덤프에서 부족한 정보 업데이트
            # TODO: In python 3.9, Channel = dumpedChannel | Channel
            for keyOfDump in dumpedChannel.keys():
                Channel.setdefault(keyOfDump, dumpedChannel[keyOfDump])
            return Channel
    print('Invalid Channel: ', Channel['Source'], '('+Channel['ServiceId']+')')
    return None

def requestEPG(Channel: Dict, config, SetDumpedChannels) -> Tuple:
    """
    올바른 ServiceId에 한해, EPG를 요청합니다. \n
    @return (Channel, SetDumpedChannels): Tuple \n
    @return Channel: Dict - 사용자가 입력한 정보와 덤프, EPG가 담긴 채널 정보 \n
    @return Channel['EPG']: List - EPG 정보. 자세한 값은 GetEPG 함수 참고 \n
    @return SetDumpedChannels: Dict - {'SourceName': DUMP}
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
            Channel['EPG'] = addEndTime(GetEPGFromSKB(Channel['ServiceId'], config['period']))      
            return (Channel, SetDumpedChannels)

        return (None, SetDumpedChannels)
        

    # LGU
    if Channel['Source'] == "LGU":
        if 'LGU' not in SetDumpedChannels:
            SetDumpedChannels["LGU"] = DumpChannelsFromLGU()
        Channel = validateChannel(Channel, SetDumpedChannels['LGU'])
        if Channel:
            Channel['EPG'] = addEndTime(GetEPGFromLGU(Channel['ServiceId'], config['fetch_period']))
            return (Channel, SetDumpedChannels)
        return (None, SetDumpedChannels)


    # NAVER
    if Channel['Source'] == "NAVER":
        if 'NAVER' not in SetDumpedChannels:
            SetDumpedChannels["NAVER"] = DumpChannelsFromNAVER()
        Channel = validateChannel(Channel, SetDumpedChannels['NAVER'])
        if Channel:
            Channel['EPG'] = addEndTime(GetEPGFromDesktopNAVER(Channel['Query'])) if config['NAVER_more_info'] else addEndTime(GetEPGFromNAVER(Channel['ServiceId'], config['fetch_period']))
            return (Channel, SetDumpedChannels)
        return (None, SetDumpedChannels)
    

    # TVING
    if Channel['Source'] == "TVING":
        if 'TVING' not in SetDumpedChannels:
            SetDumpedChannels["TVING"] = DumpChannelsFromTVING()
        Channel = validateChannel(Channel, SetDumpedChannels['TVING'])
        if Channel:
            Channel['EPG'] = addEndTime(GetEPGFromTVING(Channel['ServiceId'], config['fetch_period']))
            return (Channel, SetDumpedChannels)

        return (None, SetDumpedChannels)

    print("잘못된 Source")
    sys.exit(1)


    # WAVVE
    if Channel['Source'] == "WAVVE":
        if 'WAVVE' not in SetDumpedChannels:
            SetDumpedChannels["WAVVE"] = DumpChannelsFromWAVVE()
        Channel = validateChannel(Channel, SetDumpedChannels['WAVVE'])
        if Channel:
            Channel['EPG'] = addEndTime(GetEPGFromWAVVE(Channel['ServiceId'], config['fetch_period']))
            return (Channel, SetDumpedChannels)

        return (None, SetDumpedChannels)


# Channels = Channels.json 
try:
    with open(config['path_to_channels'], 'r', encoding='UTF-8') as file_json:
        Channels = json.load(file_json)
except Exception as e:
    print('채널 파일을 읽는 중 에러가 발생했습니다.')
    print(str(e))

# 초기화
SetDumpedChannels = None
XmlChannels = []
XmlPrograms = []

# EPG 2 XML string
for Channel in Channels:
    # UpdatedChannel은 누락된 정보와 EPG가 추가된 Channel임
    UpdatedChannel, SetDumpedChannels = requestEPG(Channel=Channel, config=config, SetDumpedChannels=SetDumpedChannels)
    if UpdatedChannel is not None:
        XmlChannels.append(writeChannel(channelInfo=Channel))
        for Program in UpdatedChannel['EPG']:
            if Program['Title'] is None: continue
            XmlPrograms.append(writeProgram(Program, UpdatedChannel['Id']))


# XML Structure
tv = Element('tv', attrib={'generator-info-name': 'pink-epg'})
for XmlChannel in XmlChannels:
    tv.append(fromstring(XmlChannel))
for XmlProgram in XmlPrograms:
    tv.append(fromstring(XmlProgram))

# Write XML
ElementTree(tv).write("xmltv.xml", encoding="UTF-8", xml_declaration=True)

# Write Dump
for source in SetDumpedChannels:
    headers = [ { 'last update': datetime.now().strftime('%Y/%m/%d %H:%M:%S'), 'total': len(SetDumpedChannels[source]) } ]
    dumps_abs_path = os.path.join(DIR, os.path.basename(config['path_to_dumps_dir']))
    
    if os.path.isfile(dumps_abs_path) == True:
        print('덤프 생성 경로와 같은 이름의 파일이 있습니다.')
        sys.exit(1)

    if os.path.isdir(dumps_abs_path) != True:
        print('해당 경로가 존재하지 않습니다.')
        sys.exit(1)
    
    with open(os.path.join(DIR, os.path.basename(config['path_to_dumps_dir']), source+'.json'), 'w', encoding='UTF-8') as jsonFile:
        jsonFile.write(json.dumps(headers + SetDumpedChannels[source], ensure_ascii=False, indent=2))
