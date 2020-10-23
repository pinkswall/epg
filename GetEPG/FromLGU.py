from typing import Dict, List
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, date
import requests
import re


def GetEPGFromLGU(serviceId: str, period: int) -> List:
    """
    LGU에서 ServiceId에 해당하는 채널의 EPG를 받아옵니다.
    """

    URL = 'http://www.uplus.co.kr/css/chgi/chgi/RetrieveTvSchedule.hpi'
    UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0'

    result = []
    p_fullTitle = re.compile(r'.+(?=\n)')
    p_title = re.compile(r'^[^[|^(^<]+')
    p_subtitle = re.compile(r'(?<=\[).+(?=\])')
    p_rebroadcast = re.compile(r'<재>')
    today = date.today()
    for day in range(period):
        target_day = today + timedelta(days=day)
        req = requests.post(URL, params={'chnlCd': serviceId, 'evntCmpYmd': target_day.strftime('%Y%m%d')}, headers={'User-Agent': UA})
        html = BeautifulSoup(req.text, 'html.parser')
        channels = html.select('.tblType > table > tbody > tr')
        
        for channel in channels:
            grade = channel.find(attrs={'class': 'tag cte_all'}).string
            KMRB = '전체관람가' if grade == 'ALL' else '12세이상관람가' if grade == '12' else '15세이상관람가' if grade == '15' else '청소년관람불가' if grade == '19' else Null

            programFullTitle = p_fullTitle.match(channel.find('td', attrs={'class': 'txtL'}).text.strip()).group()
            programTitle = p_title.search(programFullTitle).group().strip()
            subtitle = p_subtitle.search(programFullTitle).group().strip() if p_subtitle.search(programFullTitle) else None
            is_rebroadcast = True if p_rebroadcast.search(programFullTitle) else False

            result.append({
                'startTime': channel.find(attrs={'class': 'txtC'}).string.strip(),
                'programName': programTitle,
                'subtitle': subtitle,
                'category': channel.find(attrs={'class': 'txtC hidden-xs'}).string.strip(),
                'isRebroadcast': is_rebroadcast,
                'KMRB': KMRB
            })

    return result

