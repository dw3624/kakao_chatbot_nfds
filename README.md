# 화재현황 채팅봇 만들기

### 개요

 수습기자들은 수습 기간 동안 마와리를 도는 경우가 많다. 이 기간 동안 각 수습기자들은 담당 라인의 화재발생현황을 체크해야 한다. 화재발생현황은 소방청의 [국가화재정보시스템](https://nfds.go.kr/dashboard/monitor.do)에서 확인할 수 있다. 그러나 해당 사이트에서는 지역 단위로 밖에 필터링이 안 돼 직접 담당소방서를 확인해야 한다. 이에 선택한 지역에 대한 화재현황을 반환하는 챗봇을 개발해 위 과정을 간략화 시키고자 한다.

### 목표

챗봇 개발

- 지역 선택시 해당 지역 화재발생현황 반환
- 수시로 확인해야 하므로 간략한 UX 구현

### 개발환경

- 플랫폼 : kakaoTalk

- 백엔드 : python, flask

- 배포서버 : goorm IDE





## 카카오 챗봇 관리자센터

챗봇 제작 위해서는 카카오 비즈니스와 카카오 i 오픈빌더 서비스 가입이 필요함.

자세한 내용은 공식문서 [챗봇 관리자센터 준비하기](https://i.kakao.com/docs/getting-started-setup#%EC%B1%97%EB%B4%87-%EA%B4%80%EB%A6%AC%EC%9E%90%EC%84%BC%ED%84%B0-%EC%8B%9C%EC%9E%91%ED%95%98%EA%B8%B0) 참고



### [카카오 비즈니스](https://business.kakao.com/) 가입

- 약관 동의 → 정보 입력 → 가입 완료



### 카카오톡 채널 생성

- [카카오 비즈니스](https://business.kakao.com/) → 우측 상단 서비스관리 → 새 카카오톡 채널 만들기

- 새 채널 만들기 → 정보 입력 후 확인 → 채널 개설 완료

![카카오비즈니스_새채널](화재현황-채팅봇-만들기.assets/카카오비즈니스_새채널-165788398984412.PNG)

![카카오비즈니스_채널개설](화재현황-채팅봇-만들기.assets/카카오비즈니스_채널개설-165788403565414.PNG)



### [카카오 i 오픈빌더 서비스](https://i.kakao.com/)

카카오톡 채널 서비스와 연동할 챗봇은 카카오 i 오픈빌더 서비스에 가입 및 OBT 신청 후 생성 가능함.

- OBT 신청양식 작성 → OBT 신청 심사
- 가입 완료 메일 수령 → 봇 만들기



### 카카오톡 챗봇 생성

[카카오톡채널 관리자센터](https://center-pf.kakao.com/_xbdKAxj/dashboard) → 사이드메뉴 비즈니스도구 → 챗봇 → 챗봇 관리자센터 바로가기

#### 챗봇 생성

- 우측상단 봇 만들기

![챗봇생성](화재현황-채팅봇-만들기.assets/챗봇생성-165788401165813.PNG)

#### 채널 연동

- 사이드메뉴 설정 → 챗봇관리 → 카카오톡 채널 연결 → 운영/개발 채널 선택 후 저장

#### 프로필 설정

- 사이드메뉴 대시보드

![프로필설정](화재현황-채팅봇-만들기.assets/프로필설정-165788404916415.PNG)





## [goorm IDE](https://ide.goorm.io)

### 컨테이너 생성

![컨테이너생성1](화재현황-채팅봇-만들기.assets/컨테이너생성1-165788405841416.PNG)

![컨테이너생성2](화재현황-채팅봇-만들기.assets/컨테이너생성2-165788406970617.PNG)

컨테이너  실행



### flask 설치

```bash
$ root@goorm:/workspace/my_chatbot# pip insall flask
```

터미널에서 `python application.py` 실행 후 해당 URL로 접속, 결과 확인



### 포트 변경

상단메뉴 프로젝트 → 실행 URL과 포트 → 등록된 URL과 포트 → 포트 변경 → 코드 수정

```python
# application.py
...

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=<변경한 포트번호>, threaded=True)
```

터미널에서 `python application.py` 실행 후 해당 URL로 접속, 결과 확인



### 백그라운드 실행 및 종료

#### 백그라운드 실행

```bash
# chatbot 폴더의 application.py 프로그램 실행시킬 경우
$ root@goorm:/workspace/my_chatbot# nohup python3 /workspace/chatbot/application.py
```

#### 백그라운드 실행 종료

```bash
# 백그라운드 실행 중인 프로그램과 PID 확인
$ root@goorm:/workspace/my_chatbot# ps ux

# PID로 프로그램 종료
# PID 12304, COMMAND python3 /workspace/chatbot/application.py 종료시킬 경우
$ root@goorm:/workspace/my_chatbot# kill -9 PID 12304
```





## [카카오챗봇](https://i.kakao.com/)

### 용어

핵심 개념 일부 기재. 자세한 사항은 [도움말](https://chatbot.kakao.com/docs/key-concepts-entity#%EC%97%94%ED%8B%B0%ED%8B%B0%EC%9D%98-%EA%B5%AC%EC%A1%B0) 참고.

- 엔티티

  - 봇이 이해할 수 있는 용어를 정리한 데이터 사전

  ![entity-tab.png](화재현황-채팅봇-만들기.assets/entity-structure-16578786961352.png)

- 시나리오

  - 봇 안에서 사용자가 경험할 수 있는 서비스 단위
  - 예) 예금, 적금, 대출, 연금 등

- 블록

  - 사용자 의도를 응대하는 가장 작은 단위
  - 블록이 여러개 모여 시나리오 구성

- 파라미터

  - 사용자 의도를 이해하기 위해 필요한 데이터
  - API 형태로 구성되는 스킬에 보내지는 데이터

- 스킬
  - 블록에 종속돼 응답 돌려주는 기능
  - 데이터로 사용가능
  - 챗봇과 서버 API를 연결



### 실제 구현

#### 서비스플로우

- 웰컴블록
  - 메시지 : "라인을 선택해주세요"
  - 버튼 : 
    - "전체 라인 선택하기" → 전체 라인 중개 블록
    - "세부 라인 선택하기" → 세부 라인 중개 블록
- 전체 라인 중개 블록
  - 메시지 : "라인을 선택해주세요"
  - 바로가기 버튼 : 강남전체, 영등포전체, 중부, 혜북경기, 혜북서울 → 라인별 화재현황 블록
- 세부 라인 중개 블록
  - 메시지 : "세부 라인을 선택해주세요"
  - 바로가기 버튼 : 강남, 광진, 관악, 마포, 영등포, 중부, 혜북경기, 혜북서울 → 라인별 화재현황 블록
- 라인별 화재현황 블록
  - 입력 : 바로가기 버튼으로 입력된 값 → 스킬 연동
  - 응답 : 스킬데이터



#### 엔티티

![image-20220715190347698](화재현황-채팅봇-만들기.assets/image-20220715190347698-16578794319289.png)



#### 웰컴블록

![image-20220715190111666](화재현황-채팅봇-만들기.assets/image-20220715190111666-16578792738004.png)



#### 전체 라인 중개

![image-20220715190207506](화재현황-채팅봇-만들기.assets/image-20220715190207506-16578793291395.png)

![image-20220715190225093](화재현황-채팅봇-만들기.assets/image-20220715190225093.png)

![image-20220715190616807](화재현황-채팅봇-만들기.assets/image-20220715190616807-165787957930311.png)



#### 세부 라인 중개

![image-20220715190239563](화재현황-채팅봇-만들기.assets/image-20220715190239563-16578793634236.png)

![image-20220715190258618](화재현황-채팅봇-만들기.assets/image-20220715190258618.png)



#### 라인별 화재현황

![image-20220715190309437](화재현황-채팅봇-만들기.assets/image-20220715190309437-16578793908647.png)

![image-20220715190323994](화재현황-채팅봇-만들기.assets/image-20220715190323994-16578794065568.png)



#### 스킬

![image-20220715190519057](화재현황-채팅봇-만들기.assets/image-20220715190519057-165787952071010.png)



### 배포

사이드메뉴 배포 → 실시간 배포





## flask 코드

크롤링 함수 코드 `scrape_nfds.py`와 flask 메인 코드  `application.py`로 구성.

### scrape_nfds.py

국가화재정보시스템 크롤링 함수 코드

- 참조 속도 향상위해 각 라인별 소방서를 hash table구조인 dict로 저장

```python
region_dict = {
    # 강남라인
    '강남': ['강남소방서','서초소방서','송파소방서'],
    '광진': ['강동소방서','광진소방서','성동소방서'],
    
    # 영등포라인
    '관악': ['관악소방서','금천소방서','동작소방서','서초소방서'],
    '마포': ['마포소방서','서대문소방서','은평소방서'],
    '영등포': ['강서소방서','구로소방서','양천소방서','영등포소방서'],
    
    # 중부라인
    '중부': ['성북소방서','종로소방서','중부소방서','용산소방서'],
    
    # 혜북라인
    '혜북경기': [
        '가평소방서','고양소방서','구리소방서','남양주소방서','동두천소방서',
    	'양주소방서','연천소방서','의정부소방서','일산소방서','파주소방서','포천소방서'
    ],
    '혜북서울': [
        '강북소방서','노원소방서', '도봉소방서','동대문소방서','중랑소방서'
    ],    
}
```

- 크롤링한 화재현황 정보를 양식 맞춰 반환하는 함수
- 진행상태(`progressNm`)나 결과(`frfalTypeCd`)가 없는 경우 `-` 로 대체

```python
def fire_msg(res):
    tmp_ans = ''
    tmp_ans += f"일시: {res['overDate']}\n소방서: {res['cntrNm']}\n"
    tmp_ans += f"주소: {res['addr']}\n"
    tmp_ans += f"사망 / 부상: {res['dethNum']} / {res['injuNum']}\n"
    tmp_ans += f"재산피해(천원): {res['expMount']}\n"
    
    if res.get('progressNm'): progressNm = res['progressNm']
    else: progressNm = '-'
    if res.get('frfalTypeCd'): frfalTypeCd = res['frfalTypeCd']
    else: frfalTypeCd = '-'
    tmp_ans += f"진행 / 결과: {progressNm} / {frfalTypeCd}\n\n"
    
    return tmp_ans
```

- 크롤링한 각 행 정보를 `fire_msg()`로 양식에 맞게 변환 후 yield하는 generator 함수
- 속도 향상 및 메모리 효율화 위해 generator로 구현

```python
def fire_generator(res_defail, fire_stations):
    for r in res_defail:
        if r['cntrNm'] in fire_stations:
            r_msg = fire_msg(r)
            yield r_msg
```

- 크롤링 함수, 라인과 서울경기 여부 입력 받아 str형태 메시지 반환
- payload로 서울, 경기 지정
- 입력받은 라인의 소방서 목록으로 데이터 필터링

```python
def scrape_nfds(region, region_cat):
    """
    region : 지역명 - 전체 및 세부 라인명
    region_cat : s, g - 서울, 경기
    """
    url = 'https://nfds.go.kr/dashboard/monitorData.do'
    proxyDict = {
        'http'  : "add http proxy",
        'https' : "add https proxy"
    }
    
    
    # payload 설정
    if region_cat == 's':
        sido = ['11']
    elif region_cat == 'g':
        sido = ['41']
    else:
        return 'region_cat error'
    
    
    # 소방서 목록 설정
    if region == '강남전체':
        fire_stations = region_dict['강남'] + region_dict['광진']
    elif region == '영등포전체':
        fire_stations = region_dict['관악'] + region_dict['마포'] + region_dict['영등포']
    else:
        try:
        	fire_stations = region_dict[region]
        except:
            return 'region selection error'
    
    
    # 화재현황 크롤링 후 list화
    payload = {'sidoCode': sido}
    res = requests.post(url, data=payload)
    res_json = json.loads(res.text)
    if len(res_json['defail']) == 0:
        return '선택한 지역의 화재정보가 없습니다.'
    
    res_fire = fire_generator(res_json['defail'], fire_stations)
    fire_lst = list(res_fire)
    fire_msg = ''.join(f for f in fire_lst)
    if len(fire_msg) == 0:
        return '선택한 라인의 화재정보가 없습니다.'
    
    fire_msg = f'{region} 화재현황입니다.\n\n' + fire_msg
    
    return fire_msg
```



### application.py

flask 메인 코드, LineFire 스킬과 연결

- 패키지, 함수 import

```python
from flask import Flask, request, jsonify
from scrape_nfds import scrape_nfds
import sys
application = Flask(__name__)
```
- default 라우트, 스킬서버 연동 여부 확인용

```python
@application.route("/")
def hello():
    return "Hello goorm!"
```
- `request.get_json()`으로 입력된 파라미터 값 확인
- `scrape_nfds()`로 str 형태 응답 메시지 받아 json 변환 후 반환

```python
@application.route('/line-fire', methods=['POST'])
def lineDetail():
    """
    강남전체 | 영등포전체
    강남, 광진 | 관악, 마포, 영등포 | 중부 | 혜북경기, 혜북서울
    """
    req = request.get_json()
    line = req['action']['detailParams']['LineFire']['value']
    region_cat = 'g' if line == '혜북경기' else 's'
    fire_msg = scrape_nfds(line, region_cat)
        
    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": fire_msg
                    }
                }
            ]
        }
    }

    return jsonify(res)
```
- 80번 포트 사용
- `threaded=True`로 멀티스레드 허용
- `host='0.0.0.0'`으로 외부 ip로부터의 접속 허용

```python
if __name__ == "__main__":
    application.run(host='0.0.0.0', port=80, threaded=True)
```



## 기타

### 코드 개선

#### 라인 목록

- 기존 : 전체 라인과 세부 라인 함수 분리, 코드 중복 발생
  - 전체라인 : 전체, 강남전체, 영등포전체, 중부전체, 혜북전체
  - 세부 라인 : 강남, 광진, 관악, 마포, 영등포, 중부, 혜북경기, 혜북서울
- 개선 : 서울경기여부 입력값 추가해 함수 병합

- 결과 : 코드 길이 단축 및 가독성 향상

#### 응답 timeout

- 기존 :  카카오톡 응답요청시간 5초 고정, 전체 및 혜북전체 선택시 응답 timeout
- 개선 : 라인 목록서 전체, 혜북전체 제외
- 결과 : 당장의 timeout 문제 해결
- 비고 : 화재 건수 많아질 경우 timeout 발생 가능성 여전 → 데이터 처리방식 개선

#### 데이터 처리 방식

- 기존 : 크롤링 데이터 df 변환 후 데이터 처리

- 개선 : df 변환없이 json 상태로 데이터 처리
- 결과 : 코드 실행 속도 단축

#### 데이터 필터링 및 양식 변환 방식

- 기존 : 크롤링 데이터 `df.isin(<소방서목록>)`으로 필터링 후 iterrows for loop으로 양식 변환

- 개선 : generator 함수 이용해 필터링과 양식 변환 동시 진행
- 결과 : 코드 실행 속도 단축

