# covid19Vaccination

## Step1. 建立 2CAPTACHP_KEY

* 前往 [2captcha](https://2captcha.com/) ，申辦一組帳號，並除值少許錢即可，最後會獲得一組 2CAPTACHP_KEY

## Step2. 建立 config.ini 檔案，並且格式如下:

```
[personal-data]
MY_2CAPTACHP_KEY = 你的 2CAPTACHP_KEY
MY_IDENTITY_CARD = 你的身分證號碼
MY_HEALTH_ID_CARD_NUMBER = 你的健保卡卡號
MY_COOKIE = 你的 cookie
```
cookie 示意圖如下:

![image](https://user-images.githubusercontent.com/31380831/137764712-753c7bf6-3244-45fe-a0c9-72c19c046c58.png)

## Step3. 最後執行 ```py app.py``` 即可

