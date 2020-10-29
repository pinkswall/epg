from typing import Dict, List
from datetime import datetime, timedelta, date
from bs4 import BeautifulSoup
import requests
import json


def GetEPGFromNAVER(serviceId: str, period: int) -> List:
    """
    NAVER에서 ServiceId에 해당하는 채널의 EPG를 받아옵니다.\n
    @return [
        {
            'Title': '프로그램 이름',
            'Subtitle'?: '부제목',
            'StartTime': 'YYYYMMDDhhmmss +0900',
            'IsRebroadcast': True | False,
        }
    ] \n
    """

    URL = "https://m.search.naver.com/p/csearch/content/nqapirender.nhn"
    UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0'
    params = {
        'key': 'SingleChannelDailySchedule',
        'where': 'm',
        'pkid': '66',
        'u1': serviceId,
        # 'u2': '20201031'
    }
    
    for day in range(period):
        target_day = date.today() + timedelta(days=day)
        params.update({'u2': target_day.strftime('%Y%m%d')}) 

        req = requests.get(URL, params=params, headers={'User-Agent': UA})
        accuHtml = ''
        for rawHtml in json.loads(req.text)['dataHtml']:
            accuHtml = accuHtml + rawHtml
        html = BeautifulSoup(accuHtml, 'html.parser')

        channels = html.find_all(attrs={'class': 'inner'})
        result = []
        for channel in channels:
            title = channel.find('div', attrs={'class': 'pr_title'})
            startTime = channel.find('div', attrs={'class': 'time'})
            rebroadcast = channel.find('span', attrs={'class': 're'})
            subtitle = channel.find('div', attrs={'class': 'sub_info'})
            time = datetime.strptime(str(target_day) + ' ' + startTime.text.strip(), '%Y-%m-%d %H:%M').strftime('%Y%m%d%H%M%S') + ' +0900'

            program = {}

            # 필수 리턴 요소
            program.update({
                'Title': title.text.strip(),
                'StartTime': time,
                'IsRebroadcast': True if rebroadcast else False 
            })

            if subtitle: program['Subtitle'] = subtitle.text.strip()

            result.append(program)

    return result
