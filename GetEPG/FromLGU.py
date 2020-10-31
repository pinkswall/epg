from typing import Dict, List
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, date
import requests
import re


def GetEPGFromLGU(serviceId: str, period: int) -> List[Dict]:
    """
    LGU에서 ServiceId에 해당하는 채널의 EPG를 받아옵니다. \n
    @return [
        {
            'Title': '프로그램 이름',
            'Subtitle'?: '부제목',
            'Category': '카테고리',
            'StartTime': 'YYYYMMDDhhmmss +0900',
            'Episode'?: 'n회',
            'IsRebroadcast': True | False,
            'KCSC'?: '모든연령시청가' | '7세이상시청가' | '12세이상시청가' | '15세이상시청가' | '19세이상시청가'
        }
    ] \n
    @request_count: period
    """

    URL = 'http://www.uplus.co.kr/css/chgi/chgi/RetrieveTvSchedule.hpi'
    UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0'

    # Regex patterns
    p_fullTitle = re.compile(r'.+(?=\n)')
    p_title = re.compile(r'.+(?=[\(\[\<])')
    p_subtitle = re.compile(r'(?<=.\[).+(?=\])')
    p_rebroadcast = re.compile(r'<재>')
    p_episode = re.compile(r'(\d+(?=회))')

    today = date.today()
    result = []
    for day in range(period):
        target_day = today + timedelta(days=day)
        req = requests.post(URL, params={'chnlCd': serviceId, 'evntCmpYmd': target_day.strftime('%Y%m%d')}, headers={'User-Agent': UA})
        html = BeautifulSoup(req.text, 'html.parser')
        channels = html.select('.tblType > table > tbody > tr')

        for channel in channels:
            grade = channel.find(attrs={'class': 'tag cte_all'}).text.strip()
            KCSC = '모든연령시청가' if grade == 'ALL' else '7세이상시청가' if grade == '7' else '12세이상시청가' if grade == '12' else '15세이상시청가' if grade == '15' else '19세이상시청가' if grade == '19' else None

            programFullTitle = p_fullTitle.match(channel.find('td', attrs={'class': 'txtL'}).text.strip()).group()
            # TODO: need better regex
            if p_title.search(programFullTitle):
                programTitle = p_title.search(programFullTitle).group().strip()
                while p_title.search(programTitle):
                    programTitle = p_title.search(programTitle).group().strip()
            else:
                programTitle = programFullTitle
            subtitle = p_subtitle.search(programFullTitle).group().strip() if p_subtitle.search(programFullTitle) else None
            is_rebroadcast = True if p_rebroadcast.search(programFullTitle) else False
            episode = p_episode.search(programFullTitle).group().strip() if p_episode.search(programFullTitle) else None


            program = {}

            # 필수 리턴 요소
            program.update({
                'Title': programTitle,
                'Category': channel.find(attrs={'class': 'txtC hidden-xs'}).string.strip(),
                'StartTime': datetime.strptime(str(target_day) + ' ' + channel.find(attrs={'class': 'txtC'}).string.strip(), '%Y-%m-%d %H:%M').strftime('%Y%m%d%H%M%S') + ' +0900',
                'IsRebroadcast': is_rebroadcast
            })

            if subtitle: program['Subtitle'] = subtitle
            if episode: program['Episode'] = episode
            if KCSC: program['KCSC'] = KCSC
            
            result.append(program)

    return result