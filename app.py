import requests
import json
import base64
import shutil
import time
import configparser

# 為了保護個人資料，故而將隱密資料寫入 config.ini 檔案中
config = configparser.RawConfigParser()
config.read('config.ini') 

API_KEY = config.get('personal-data', 'MY_2CAPTACHP_KEY') # 你的 2captcha API_KEY
idn = config.get('personal-data', 'MY_IDENTITY_CARD') # 你的身分證
nhCard = config.get('personal-data', 'MY_HEALTH_ID_CARD_NUMBER')  # 你的健保卡號
headers = {
    "cookie": config.get('personal-data', 'MY_COOKIE'), # "執行身分認證" 按鈕後的 cookie
    "authority": "vab.1922.gov.tw",
    "sec-ch-ua": 'Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
    "accept": "application/json, text/javascript, */*; q=0.01",
    "content-type": "application/json; charset=UTF-8",
    "x-requested-with": "XMLHttpRequest",
    "sec-ch-ua-mobile": "?0",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36",
    "sec-ch-ua-platform": "Windows",
    "origin": "https://vab.1922.gov.tw",
    "sec-fetch-site": "same-origin",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "referer": "https://vab.1922.gov.tw/vab/?language=ch",
    "accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,und;q=0.6"
}
validateCodeResp = requests.get("https://vab.1922.gov.tw/vab/validateCodeService.do", headers = headers,  stream=True)
if validateCodeResp.status_code == 200:
    with open("captcha.png", 'wb') as f:
        validateCodeResp.raw.decode_content = True
        shutil.copyfileobj(validateCodeResp.raw, f) 
file = {'file': open('captcha.png', 'rb')}
captchaInResp = requests.post('http://2captcha.com/in.php', files = file, params = { 'key': API_KEY }) 
if captchaInResp.ok and captchaInResp.text.find('OK') > -1:
    captcha_id = captchaInResp.text.split('|')[1]
    for i in range(10):
        print(f'驗證碼執行了 {i+1} 次了')
        captchaResResp = requests.get(f'http://2captcha.com/res.php?key={API_KEY}&action=get&id={captcha_id}')
        if captchaResResp.text.find('CAPCHA_NOT_READY') > -1:  # 尚未辨識完成
            time.sleep(3)
        elif captchaResResp.text.find('OK') > -1:
            captcha_text = captchaResResp.text.split('|')[1]
            print(f'驗證碼為 {captcha_text}')
            payload = {
                    "idn": idn,
                    "certTp":"1",
                    "houhldPfn":"",
                    "seal":"",
                    "inqCode":"",
                    "born":"",
                    "nm":"",
                    "name":"",
                    "nhicBaseData":"",
                    "nhicHSign":"",
                    "nhicRandomNo":"",
                    "nhicPassword":"",
                    "checkCode":captcha_text,
                    "otpCode":"",
                    "nhCard":nhCard,
                    "passportNo":"",
                    "licenseNo":""
                }
            logiRresp =  requests.request("POST", "https://vab.1922.gov.tw/vab/payerLoginService.do", json = payload, headers = headers)
            print(f'最終結果為 {logiRresp.json()}')
            break
        else:
            print('取得驗證碼發生錯誤!')
