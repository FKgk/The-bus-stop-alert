import telegram
import time
from dialogflow.models import User_infomation, Bus_cancel_list
from . import kwang

my_token = '528073731:AAF3XW096WI_CMoZmNio_rcBJHWSGFuUMbc'
bot = telegram.Bot(token = my_token)
my_webhook = bot.get_webhook_info()

'''
def start_webhook():
    bot.set_webhook(my_webhook.url, True)
    print('webhook true')
    
def finish_webhook():
    bot.set_webhook()
    print('webhook false')
''' 

def set_start_number(telegram_chat_id, terminate):
    start = "광운대학교" # 임의 지정
    number = "261" # 임의 지정
    print("set_start_number0")
    get_bus(start, terminate, number, telegram_chat_id)
    print("set_start_number1")
    return None
    
def status_change(telegram_chat_id):
    print("사용자의 상태 값을 변경하겠습니다.")
    Bus_cancel_list(user_id = telegram_chat_id, status = False, bus_num = 0).save()
    db = Bus_cancel_list.objects.get(user_id = telegram_chat_id)
    mess = "user database status : " + str(db)
    print(mess)
    
    return None

def get_bus(start, terminate, number, chat_id): # actionds에 의해 실행되는 함수
    '''
    print('bus 실행')
    try: # webhook이 꺼지면 안되기 때문에 예외처리 적용 
        finish_webhook()
    #update에 값이 없으면 계속 getUpdates()실행
        updates = bot.getUpdates()
        print('updates 한번 실행')
        count = 0
        while not updates: # updates에 내용이 없으면 True
            #print(type(updates))
            #print(updates)
            count += 1
            print(count,'만큼 실행')
            time.sleep(1)
            try:
                updates = bot.getUpdates() # timeout - 시간 조정
            except:
                print('updates 에러')
            #print('updates 중')
            
        print('알림 입력 받았습니다.')
    except:
        # 알람 
        print('에러가 발생 예외처리')
        return None
    finally:
        try:
            start_webhook()
        except:
            print('webhook 에러')
            
    chat_id = updates[-1].message.chat.id
'''
    #print(chat_id)
    
    # 사용자로부터 입력된 값을 데이터베이스에 저장
    User_infomation(start = start, terminate = terminate, bus_num = number, user_id = chat_id).save()
    Bus_cancel_list(start = start, terminate = terminate, bus_num = number, user_id = chat_id).save()
    print("사용자의 값을 데이터베이스에 추가했습니다.")
    # kwang 파일의 함수를 호출
    kwang.get_bus_time(start, terminate, number, chat_id, bot)
    
    return None