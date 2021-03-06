import json
import requests
from bs4 import BeautifulSoup


def DumpChannelsFromNAVER():
  """
  네이버에서 제공하는 EPG의 채널 목록을 파싱합니다. \n
  @return [ 
    {
      'Name': '채널이름',
      'Source': 'NAVER',
      'ServiceId': '서비스ID',
      'Query': 'Search Term'
    }
  ] \n
  @request_count: 6
  """

  print('Naver에서 정보를 가져오고 있습니다 . . .')

  URL = "https://m.search.naver.com/p/csearch/content/nqapirender.nhn"
  UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0'
  category = [
    {'name': '지상파', 'u1':'100'},
    {'name': '종합 편성', 'u1': '500'},
    {'name': '케이블', 'u1': '200'},
    {'name': '스카이라이프', 'u1': '300'},
    {'name': '해외위성', 'u1': '9000'},
    {'name': '라디오', 'u1': '400'}
  ]


  result = []
  for cat in category:
    params = {
      'pkid': '66',
      'where': 'nexearch',
      'u1': cat['u1'],
      'key': 'ScheduleChannelList'
    }
    
    try:
      req = requests.get(URL, headers={'User-Agent': UA}, params=params)
      print('Status Code: ', req.status_code)
    except Exception as e:
      print('API 요청 중 에러: %s' % str(e))

    html = BeautifulSoup(json.loads(req.text)['dataHtml'], 'html.parser')
    channels = html.select('li.item')

    for channel in channels:
      ch_name = channel.find('div', attrs={'class': "channel_name"}).string
      ch_id = channel.find('div', attrs={'class': "u_likeit_list_module _reactionModule zzim"})['data-cid']
      ch_query = channel.find('a', attrs={'class': 'lk'})['href']

      result.append({
        'Name': str(ch_name).strip(),
        'Source': 'NAVER',
        'ServiceId': ch_id.strip(),
        'Query': ch_query.strip()
      })
  
  return result
