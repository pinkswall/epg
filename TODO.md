# TO IMPLEMENT

## Todo-list

| Source | Dump   | EPG    |
| ------ | ------ | ------ |
| KT     | 미지원 | 미지원 |
| SKB    | 지원   | 미지원 |
| LGU    | 지원   | 지원   |
| NAVER  | 지원   | 미지원 |
| DAUM   | 미지원 | 미지원 |
| WAVVE  | 지원   | 미지원 |
| TVING  | 지원   | 미지원 |

- 모두 지원하기 !

- argparse 적용

- logging system

- comprehension 문법

- Id가 없다면 임의로 지정

- 문서화 !

- 정확한 타입 지정(typing)

- 각 EPG의 period limit 처리

- 1부, 2부 나뉠시 통합하는 옵션 추가 (자세한 내용은 [클릭](https://www.clien.net/service/board/cm_nas/12566572))

- html parsing을 정규식으로.. (bs4 대체)

## Things To Look for

- imdb, thetvdb 사용가능 여부  
   -> imdb는 한국어 미지원으로 사용불가.  
   -> thetvdb는 극소수이지만 데이터가 있는듯?
  </br>
- Id가 tvheadend에서 어디에 쓰이는지. 정말 채널과 프로그램 매칭에만 쓰이나?
- KT는 IPTV상품에 따라 ServiceId가 다른듯 하다. 가장 많은 채널을 지원하는 상품은 어느 상품이지?
- Naver Dump에서 중복되는 채널을 찾았다. 스카이라이프 탭에서 중복되는 채널을 제공하기 때문이다. 채널 이름은 같은걸로 보이지만 ServiceId가 다르다. 이 때문에 다른 문제가 생길 수 있는지?

## Todo-now

- 네이버 EPG 함수 구현
