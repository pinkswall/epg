# GetEPG

## 지금은?

| Source | EPG    | max period |
| ------ | ------ | ---------- |
| KT     | 미지원 | ?          |
| SKB    | 미지원 | ?          |
| LGU    | 지원   | 5          |
| NAVER  | 지원   | 6 (+어제)  |
| DAUM   | 미지원 | ?          |
| WAVVE  | 미지원 | ?          |
| TVING  | 미지원 | ?          |

max period에 당일 날짜도 포함됩니다.  

## Output

- Title: 프로그램 명
- Category?: 카테고리
- StartTime: YYMMDDhhmmss +0900
- IsRebroadcast: True | False
- Subtitle?: 부제목
- Icon_url?: 프로그램 icon url
- Episode?: n(회)
- KCSC?: [방송법 제33조(심의규정)](https://www.law.go.kr/%ED%96%89%EC%A0%95%EA%B7%9C%EC%B9%99/%EB%B0%A9%EC%86%A1%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%A8%EC%9D%98%EB%93%B1%EA%B8%89%EB%B6%84%EB%A5%98%EB%B0%8F%ED%91%9C%EC%8B%9C%EB%93%B1%EC%97%90%EA%B4%80%ED%95%9C%EA%B7%9C%EC%B9%99)

## 특이사항

네이버 모바일에서는 시청등급과 회차를 제공하지 않는다.
