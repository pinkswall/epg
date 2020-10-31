from typing import Dict, List
from datetime import datetime, timedelta, date
from bs4 import BeautifulSoup
import requests
import re

def GetEPGFromDesktopNAVER(Query: str) -> List:
  """
  NAVER Desktop 페이지에서 ServiceId에 해당하는 채널의 EPG를 받아옵니다.\n
  @return [
      {
          'Title': '프로그램 이름',
          'Subtitle'?: '부제목',
          'Episode'?: 'n'
          'StartTime': 'YYYYMMDDhhmmss +0900',
          'IsRebroadcast': True | False,
          'KCSC'?: '7세이상시청가' | '12세이상시청가' | '15세이상시청가' | '19세이상시청가'
      }
  ] \n
  """
  
  URL = "https://search.naver.com/search.naver" + Query
  UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0"
  req = requests.get(URL, headers={'User-Agent': UA})
  html = BeautifulSoup(req.text, 'html.parser')
  
  Hours = html.select('.program_list > li.item')
  
  # Regex patterns
  p_title = re.compile(r'.+(?=\()')
  p_episode = re.compile(r'(\d+(?=회))')


  result = []

  # 하루씩 처리
  for a in range(1, 8):
    # 시간 
    for Hour in Hours:
      pr_hour = Hour.find('div', attrs={'class':'time_box'}).text.strip()
      programs = Hour.find_all('div', attrs={'class': 'col' + str(a)})

      for program in programs:
        # HTML Elements
        el_min = program.find('div', attrs={'class': 'time_min'})
        el_titleWithEpisode = program.find(attrs={'class': 'pr_title'})
        el_subtitle = program.find('span', attrs={'class': 'pr_sub_title'})
        el_grade = program.find('span', attrs={'class': 'age_icon'})
        el_rebroadcast = program.find('span', attrs={'class': 's_label re'})

        # Strings about program or None
        pr_min = el_min.text.strip()
        pr_titleWithEpisode = el_titleWithEpisode.text.strip()  if el_titleWithEpisode else None
        pr_subtitle = el_subtitle.text.strip() if el_subtitle else None
        pr_grade = el_grade.text.strip() if el_grade else None

        if pr_titleWithEpisode == '': continue

        # Processing
        Title = p_title.search(pr_titleWithEpisode).group() if p_title.search(pr_titleWithEpisode) else pr_titleWithEpisode
        Episode = p_episode.search(pr_titleWithEpisode)
        StartTime = datetime.strptime(str(date.today() + timedelta(days=a-2)) + ' ' + pr_hour + pr_min , '%Y-%m-%d %H시%M분').strftime('%Y%m%d%H%M%S') + ' +0900'
        IsRebroadcast = True if el_rebroadcast else False
        KCSC = None if (pr_grade is None) or (pr_grade == '') else pr_grade + '이상시청가'

        singleEPG = {
          'Title': Title,
          'StartTime': StartTime,
          'IsRebroadcast': IsRebroadcast
        }
        if Episode: singleEPG['Episode'] = Episode.group()
        if KCSC: singleEPG['KCSC'] = KCSC
        if pr_subtitle: singleEPG['Subtitle'] = pr_subtitle

        result.append(singleEPG)
  return result
