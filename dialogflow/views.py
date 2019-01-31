from pprint import pprint
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from . import actions
# from .models import Pizza
import json
import telegram
import random
from dialogflow.models import Alarm, Bus_cancel_list

my_token = ''

bot = telegram.Bot(token = my_token)
#bot.send_photo(chat_id = 658598942,
#        photo = "")

def index(request):
    return render(request, 'dialogflow/index.html', {
        'WEB_DEMO_URL': settings.DIALOGFLOW['WEB_DEMO_URL'],
    })

def sendMsg(chat_id, name, card_id, ad):
    start = "광운대학교"
    
    print("start : " + start)
    print("bus : 261 \n")
    print("Send Message to User \n")
    
    bot.sendMessage(chat_id = chat_id, text = name + "님 안녕하세요!" + '\n\n' + "방금 " + start + "(석계역 방향) 정류장에서 261번 버스에 승차하셨어요. 도착 정류장을 '알림'과 함께 입력해주시면 해당 버스가 도착 정류장에 가까워졌을 때 알림 메시지를 전송해드립니다 (ex. 석계역 알림)" + '\n\n' + ad)
    Alarm(user_id = chat_id, card_id = "card_id", status = True).save()
    print("데이터베이스에 저장했습니다.")
    bot.sendPhoto(chat_id = chat_id, photo = "https://photos.app.goo.gl/1dtq6jvB2p4KyMXY7", caption = "261번 버스 노선도")
    
@csrf_exempt
@require_POST
def fulfillment(request):
    # request.JSON: intent에서 먼저 처리한 내역
    action_name = request.JSON['result']['action'].replace('-', '_')
    params = request.JSON['result']['parameters']
    cnt = 0
    print("fulfillment")
    print(type(request))
    print(request.read().decode('utf8'))
    try:
        telegram_chat_id = request.JSON['result']['contexts'][0]['parameters']['telegram_chat_id']
        print(request.JSON['result']['contexts'][0])
    except:
        try:
            telegram_chat_id = request.JSON['result']['contexts'][1]['parameters']['telegram_chat_id']
            print(request.JSON['result']['contexts'][1])
            #print('telegram_chat_id 잘 가져왔습니다.')
        except:
            try:
                telegram_chat_id = request.JSON['result']['contexts'][2]['parameters']['telegram_chat_id']
                print(request.JSON['result']['contexts'][2])
            except:
                #print('telegram_chat_id [2] key 에러')
                return request.JSON['result']['contexts']
        
    if action_name == "alarm_search":
        terminate = params['terminate']
        actions.alarm_search(telegram_chat_id, terminate)
        return str(0)
    elif action_name == "cancel":    #취소 입력시
        actions.bus_cancel(telegram_chat_id)
        return str(0)
        
    try:
        if params['start']:    # 값이 없는 것에 대한 처리 미흡(key error)
            start = params['start']
            terminate = params['terminate']
            number = params['number']
            cnt = 1
    except:
        pass
    

    action = getattr(actions, action_name, None)

    '''
    return {
        'speech': params['start']
    }
    '''
    if cnt == 1:
        speech = action(start, terminate, number, telegram_chat_id)    
    elif callable(action):
        speech = action(**params)
    else:
        speech = '제가 처리할 수 없는 부분입니다.'
    
    return {
        'speech': speech,
    }

# Card UID:149 174 27 17  VISA 카드 - 홍찬
# Card UID:63 63 39 34   휴대폰 - 승연
# Card UID:115 8 85 82  휴대폰 - 광호

ad1 = "[광고] 홍찬토익 등록시 100% 할인"
ad2 = "[광고] 강승연헤어두 10월까지 100% 세일"
ad3 = "[광고] 취업률 100% 광호대학교 수시모집 중"
ads = [ad1, ad2, ad3]

def aduino_yhc(request):
    chat_id = 637980973
    db = Bus_cancel_list.objects.get(user_id = chat_id)
    chTime = Alarm.objects.get(user_id = chat_id)
    
    print("YHC INIT UESER STATUS : " + str(db))
    print("YHC INIT USER TIME : " + str(chTime))
    
    if str(db) == str(True):
        return str(chTime)
    else:
        num = random.randrange(0,3)
        sendMsg(chat_id, "윤홍찬", "149 174 27 17" , ads[num])
        return str(25)

def aduino_ksy(request):
    chat_id = 512006009
    db = Bus_cancel_list.objects.get(user_id = chat_id)
    chTime = Alarm.objects.get(user_id = chat_id)
    
    print("KSY INIT UESER STATUS : " + str(db))
    print("KSY INIT USER TIME : " + str(chTime))
    
    if str(db) == str(True):
        return str(chTime)
    else:
        num = random.randrange(0,3)
        sendMsg(chat_id, "강승연", "63 63 39 34" , ads[num])
        return str(25)

def aduino_kkh(request):
    chat_id = 658598942
    db = Bus_cancel_list.objects.get(user_id = chat_id)
    chTime = Alarm.objects.get(user_id = chat_id)
    
    print("KKH INIT UESER STATUS : " + str(db) )
    print("KKH INIT USER TIME : " + str(chTime) )
    
    if str(db) == str(True):
        return str(chTime)
    else:
        num = random.randrange(0,3)
        sendMsg(chat_id, "김광호", "115 8 85 82" , ads[num])
        return str(25)
    
def message_ksy(request):
    chat_id = 512006009
    db = Bus_cancel_list.objects.get(user_id = chat_id)
    chTime = Alarm.objects.get(user_id = chat_id)
    
    print("KSY message UESER STATUS : " + str(db) )
    print("KSY message USER TIME : " + str(chTime) )
    
    if str(db) == str(True):
        return str(chTime)
    else:
        return str(0)

def message_yhc(request):
    chat_id = 637980973
    db = Bus_cancel_list.objects.get(user_id = chat_id)
    chTime = Alarm.objects.get(user_id = chat_id)
    
    print("YHC message UESER STATUS : " + str(db) )
    print("YHC message USER TIME : " + str(chTime) )
    
    if str(db) == str(True):
        return str(chTime)
    else:
        return str(0)

def message_kkh(request):
    chat_id = 658598942
    db = Bus_cancel_list.objects.get(user_id = chat_id)
    chTime = Alarm.objects.get(user_id = chat_id)
    
    print("KKH message UESER STATUS : " + str(db) )
    print("KKH message USER TIME : " + str(chTime) )
    
    if str(db) == str(True):
        return str(chTime)
    else:
        return str(0)
