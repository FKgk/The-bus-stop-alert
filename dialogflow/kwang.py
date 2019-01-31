import pandas as pd
from bs4 import BeautifulSoup
import requests
import time
import telegram
from dialogflow.models import Bus_cancel_list, Alarm
import random

def get_html(url, APIKEY,request_name, request):
    request_url = url + APIKEY + request_name + request
    req = requests.get(request_url)
    html = req.text
    return BeautifulSoup(html, 'html.parser')

def get_time(text):
    sec = 0
    for i in range(len(text)):
        if text[i] == '분':
            try:
                sec = int(text[0:i]) * 60
                a = i
            except:
                #print('시간 측정에서 에러발생', text)
                return 10
        elif text[i] == '초':
            sec += int(text[a+1:i])
            break
    return sec

def getUserDatabaseStatus(chat_id):
    db = Bus_cancel_list.objects.get(user_id = chat_id)
    return str(db)
    #mess = "user database status : " + str(db)
    #print(mess)

bus_info_APIKEY = ''
# 1: 광호, 2: 홍찬, 3: 승연
station_info_APIKEY = [
    '', 
    '',
    '',
]
#버스 ID 가져오기
bus_info_getRoutePathList_url = 'http://ws.bus.go.kr/api/rest/busRouteInfo/getBusRouteList?serviceKey=' # 요청 URL
getBusRouteList_request = '&strSrch=' # 요청 변수
#버스 정류장 가져오기
bus_info_getStaionsByRouteLis_url = 'http://ws.bus.go.kr/api/rest/busRouteInfo/getStaionByRoute?serviceKey='
getStaionsByRouteList_request = '&busRouteId='
# 버스 정류장으로 버스 고유 id 가져오기
bus_station_info_url = 'http://ws.bus.go.kr/api/rest/stationinfo/getStationByUid?serviceKey='
getStationByUidItem_request = '&arsId='
#while문 무한 루프
#cnt = True
#my_token = ''
#bot = telegram.Bot(token = my_token)

# 입력 받기
def get_bus_time(start_name, end_name, bus_name, chat_id, bot):
    print("Kwang.get_bus_time")
    db = Bus_cancel_list.objects.get(user_id = chat_id)
    #print(type(db))
    API_KEY_number = random.randrange(0,3)
    busRouteId = None # 버스 노선 ID
    bus_station = {start_name : None, end_name : None} # 에러 발생 TypeError: unhashable type: 'list'
    cnt = True
    # 시작 정류장 도착 정류장 번호
    vehid = None # 차량 고유 ID    
    """   
    # 노선 이름 검색
        soup = get_html(bus_info_getRoutePathList_url, bus_info_APIKEY, getBusRouteList_request, bus_name)
        print("노선 이름 검색")
        # 노선 이름이 잘못되서 아무것도 검색이 안되었을 때 여러개 있을 경우 - 생각하지 않음 나중에 수정
        try: busRouteId = (soup.find_all('busrouteid'))[0].text # 인덱스를 넘었을 경우 아무것도 없을 경우
        except:
            bot.sendMessage(chat_id = chat_id, text = '버스 이름이 잘못 되었습니다. 처음부터 다시 시작해주세요.')
            return None
    """
    busRouteId = "100100043"
    # 노선 아이디로 정류장 목록 가져오기
    soup = get_html(bus_info_getStaionsByRouteLis_url, bus_info_APIKEY, getStaionsByRouteList_request, busRouteId)
    station_name = soup.find_all('stationnm') #정류소 이름
    station = soup.find_all('station') # 정류소 Id
    station_arsid = soup.find_all('arsid')# 정류소 고유번호
    print("노선 ID 가져오기")
    
    num = len(station_name)

    # 노선 방향 결정
    for i in range(num):
        if station_name[i].text == start_name:
            bus_station[start_name] = i
        elif not bus_station[start_name] == None and station_name[i].text == end_name:
            bus_station[end_name] = i
            break
    # 정류장 이름이 잘 못 되었습니다.
    if bus_station[start_name] == None:
        bot.sendMessage(chat_id = chat_id, text = "시작 정류장 이름이 잘못되었습니다. 다시 입력해주세요.")
        return None
    if bus_station[end_name] == None:
        bot.sendMessage(chat_id = chat_id, text = "도착 정류장 이름이 잘못되었습니다. 다시 입력해주세요.")
        return None
    print("정류장 예외 처리")

    soup = get_html(bus_station_info_url, station_info_APIKEY[API_KEY_number], getStationByUidItem_request,station_arsid[bus_station[start_name]+1].text)
    station_busRouteId = soup.find_all('busrouteid')
    unique_bus_id = soup.find_all('vehid1') # 현재 차량ID
    print("현재 차량 ID")
    for i in range(len(station_busRouteId)):
        if station_busRouteId[i].text == busRouteId:
            vehid = unique_bus_id[i].text
            break
    if vehid == None: # unique bus_id 가 list 형 이면
        bot.sendMessage(chat_id = chat_id, text = "시작 정류장을 지날 수 있는 버스가 없습니다.")
        return None
    print('노선 ID', busRouteId)
    print('차량 ID', vehid)
    print('시작 정류장 앞 고유 번호',station_arsid[bus_station[start_name]+1].text)
    print('도착 정류장 고유 번호',station_arsid[bus_station[end_name]].text)
    end_station_arsid = station_arsid[bus_station[end_name]].text

    '''
    busRouteId - 노선 ID
    vehid - 차량 ID
    end_station_arsid - 도착 정류장 고유 번호

    '''
    
    bot.sendMessage(chat_id = chat_id, text = '알림 서비스가 시작되었습니다. 버스가 목적지에 가까워지면 알림 메시지가 수신됩니다.')
    
    while db: # 데이터 베이스에서 값 가져와서 비교하기
        #mess = "user status : " + str(db)
        #print(mess)
        db = Bus_cancel_list.objects.get(user_id = chat_id)
            
        
        soup = get_html(bus_station_info_url, station_info_APIKEY[API_KEY_number],  getStationByUidItem_request, end_station_arsid)
        station_busRouteId = soup.find_all('busrouteid')# 노선 ID
        temp_vehid = soup.find_all('vehid1')# 차량 고유 번호
        bus_status1 = soup.find_all('arrmsg1')# 첫 번째 버스 상태

        for i in range(len(station_busRouteId)):
            if station_busRouteId[i].text == busRouteId: #노선ID가 같은 번쨰 찾기
                print(bus_status1[i].text)
                #bot.sendMessage(chat_id = chat_id, text = bus_status1[i].text)
                break_time = get_time(bus_status1[i].text)
            
                if vehid == temp_vehid[i].text : # 고유 번호가 맞는 지 확인
                    if bus_status1[i].text == "곧 도착":# 버스 상태가 '곧 도착'이면 출력하고 종료
                        cnt = False
                        #print('진입 차량이 내가 탄 차량이고 곧 도착한다')
                        print(bus_status1[i].text + " " + chat_id)
                        destination = "%s번 버스가 %s에 곧 도착합니다. 하차 준비하세요." % (bus_name, end_name)
                        bot.sendMessage(chat_id = chat_id, text = destination)
                        
                        print("사용자의 상태 값을 변경하겠습니다.")
                        
                        Alarm(user_id = chat_id, time = 0).save()
                        finalTime = Alarm.objects.get(user_id = chat_id)
                        msg = "user database time : " + str(finalTime)
                        print(msg)
                        
                        time.sleep(15)
    
                        Bus_cancel_list(user_id = chat_id, status = False, bus_num = 0).save()
                        getUserDatabaseStatus(chat_id)
                        print("user database status : " + str(db))
                        
                        return None
                    elif bus_status1[i].text == '운행 종료':
                        bot.sendMessage(chat_id = chat_id, text = "버스가 운행 종료 되었습니다.")
                        return none
                    elif bus_status1[i].text == '출발 대기':
                        bot.sendMessage(chat_id = chat_id, text = "버스가 아직 출발되지 않았습니다.")
                        return none
                    else: # 정류장에 가는 첫 번째 버스이지만 곧 도착이 아니면 쉬기
                        print('진입 차량이 내가 탄 차량이지만 곧 도착이 아니라서',break_time,'이지만', int(break_time/3),'만큼 쉬기')
                        
                        # 데이터베이스 값 sleep시간으로 변경
                        Alarm(user_id = chat_id, time = break_time/3).save()
                        chTime = Alarm.objects.get(user_id = chat_id)
                        print("user database time : " + str(chTime))
                        getUserDatabaseStatus(chat_id)
                        print("user database status : " + str(db))
                        #bot.sendMessage(chat_id = chat_id, text = '진입 차량이 내가 탄 차량이지만 곧 도착이 아니다')
                        time.sleep(int(break_time/3))
                        
                else: # 진입 차량이 내가 탄 차량이 아니다
                    print('진입 차량이 내가 탄 차량과 다르다')
                    print(break_time,'이지만',int(break_time/2 + 25),'만큼 쉬기')
                    #bot.sendMessage(chat_id = chat_id, text = '진입 차량이 내가 탄 차량과 다르다 %f초만큼 쉬기'%(break_time/2+10))
                    # 데이터베이스 값 10으로 변경
                    Alarm(user_id = chat_id, time = 25).save()
                    chTime = Alarm.objects.get(user_id = chat_id)
                    print("user database time : " + str(chTime))
                    getUserDatabaseStatus(chat_id)
                    print("user database status : " + str(db))
                    
                    time.sleep(int(break_time/2 + 25))
                break
    bot.sendMessage(chat_id = chat_id, text = '알림 서비스가 취소되었습니다.')
    return None