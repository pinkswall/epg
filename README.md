# epg2xml

파이썬 연습과 개인적 필요에 의한 레포입니다.  
NAVER, DAUM, KT, SKB, LGU, WAVVE, TVING 지원을 목표로 합니다. <br/>

## 사용하기 전에

> pip install requests beautifulsoup4

## 요청 횟수

| Source | 요청 횟수<sup id="q1">[1](#a1)</sup>       |
| ------ | ------------------------------------------ |
| KT     | `None`                                     |
| SKB    | `None`                                     |
| LGU    | `#channels * #period + 9`                  |
| NAVER  | `#channels + 6`<sup id='q2'>[2](#a2)</sup> |
| DAUM   | `None`                                     |
| WAVVE  | `None`                                     |
| TVING  | `None`                                     |

<sup><b id="a1">1. </b>(EPG를 가져오는데 필요한 요청 횟수) + (DUMP에 필요한 요청 횟수) [↩](#q1)</sup>  
<sup><b id="a2">2. </b>한 요청에 7일치 EPG를 가져옵니다. [↩](#q2)</sup>

## 특징

- ServiceID와 Source만 있어도 작동합니다. 누락된 정보는 해당 소스의 덤프를 바탕으로 자동으로 기입됩니다.
- EPG를 요청하기 전에 잘못 기입된 채널을 걸러냅니다.

# TODO

| Source | Dump   | EPG    |
| ------ | ------ | ------ |
| KT     | 미지원 | 미지원 |
| SKB    | 지원   | 미지원 |
| LGU    | 지원   | 지원   |
| NAVER  | 지원   | 지원   |
| DAUM   | 미지원 | 미지원 |
| WAVVE  | 지원   | 미지원 |
| TVING  | 지원   | 미지원 |
