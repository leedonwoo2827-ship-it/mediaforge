# 왜 FlowGenie는 합치지 않고 따로 두나

## 결론
FlowGenie는 mediaforge **안에 넣을 수 없다.** 합치는 게 아니라 **역할을 나누고 파일로
연결**한다. 그래서 mediaforge를 어떤 프레임워크로 만들든 FlowGenie와는 무관하다.

## 이유
- **FlowGenie = 크롬 확장**: Google Flow(labs.google/flow) 페이지 위에서, **구글 로그인
  세션**에 올라타 동작한다. 브라우저 안에서만 돈다.
- **mediaforge = 로컬 파이썬 웹앱**: 내 PC의 별도 프로세스. 브라우저 로그인과 무관.
- 파이썬 코드가 "구글에 로그인해 Flow를 조작"하게 만들 수 없다(로그인·iframe 차단·약관).
  그래서 이미지 생성만은 **사람이 브라우저에서** 한다.

## 연결 방식 (유일한 접점)
```
FlowGenie(크롬 확장)  →  이미지를  ~/Downloads/FlowGenie/  에 저장
                                  │
mediaforge "📥 가져오기"  ────────┘  파일을 읽어 번들 images/ 로 복사
```
- 접점은 **다운로드 폴더 + 파일명 규칙(chNN_XX_*)** 하나뿐.
- 그래서 "공존"이 아니라 **분업**이다. FlowGenie는 지금처럼 브라우저에서 그대로 쓴다.

## mediaforge는 크롬 확장이 아니다
`run.bat` 으로 켜고 `http://localhost:7878` 로 접속하는 로컬 웹앱이다. 크롬에 설치하는
것은 FlowGenie 하나뿐.

## 한 가지 자동화 (편의)
여러 번 재생성해 `_1,_2,…` 가 쌓이면, 가져오기는 **가장 최근(마지막) 1장**만 골라온다.
([../ingest/import_images.py](../ingest/import_images.py))
