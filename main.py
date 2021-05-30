import requests
import telegram
import time
import traceback
import json

with open("config.json") as f:
    config = json.loads(f.read())

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.37'}

# Telegram
telegram_token = config["telegram_token"]
telegram_chat_id = config["telegram_chat_id"]
telegram_bot = telegram.Bot(token=telegram_token)

def chk_stock(prdt_code, zip_code): # 모델명과 우편번호 입력하여 재고 확인
    url = f'https://www.apple.com/kr/shop/fulfillment-messages?pl=true&parts.0={prdt_code}&location={zip_code}'
    res = requests.get(url, headers=headers).json()
    stores = res['body']['content']['pickupMessage']['stores']

    stock = False
    global prdt_name

    for store in stores:
        pickup_stock = store['partsAvailability'][prdt_code]['storePickupQuote']
        prdt_name = store['partsAvailability'][prdt_code]['storePickupProductTitle']
        if pickup_stock != 'Apple 매장 픽업은 현재 이용할 수 없음':
            stock = True
    return stock

def telegram_send(message): # 텔레그램 메시지 전송
    telegram_bot.sendMessage(chat_id=telegram_chat_id, text='[애플 재고 확인]\n'+message)

prdt_name = ''
prdt_code = 'MHNF3KH/A'
zip_code = config['zip_code']
repeat = 5
telegram_send('프로그램 시작')

while True:
    try:
        if chk_stock(prdt_code, zip_code):
            message = f'제품명: {prdt_name}\n모델명: {prdt_code}\n입고 확인'
            telegram_send(message)
            for i in range(repeat-1):
                time.sleep(1)
                telegram_send(message)

    except Exception as e:
        telegram_send(f'🚨 에러 발생\n{traceback.format_exc()}')

    time.sleep(5)
