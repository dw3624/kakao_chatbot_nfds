import requests
import json


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


def fire_msg(res):
    """
    각 행 정보를 메시지 양식으로 변환
    """
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
    

def fire_generator(res_defail, fire_stations):
    """
    generator 함수, 각 행 정보를 msg로 변환 후 yield
    """
    for r in res_defail:
        if r['cntrNm'] in fire_stations:
            r_msg = fire_msg(r)
            yield r_msg


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
#     if region == '전체':
#         pass
    if region == '강남전체':
        fire_stations = region_dict['강남'] + region_dict['광진']
    elif region == '영등포전체':
        fire_stations = region_dict['관악'] + region_dict['마포'] + region_dict['영등포']
#     elif region == '중부전체':
#         fire_stations = region_dict['중부']
#     elif region == '혜북전체':
#         pass
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