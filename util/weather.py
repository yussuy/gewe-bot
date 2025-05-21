import requests
import json
def getWeather(date):
    url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/xxxxxxxxxxxxx' + date
    params = {
        'lang': 'zh',
        'unitGroup': 'metric',
        'key': 'xxxxxxxxxxxxx'
    }
    weather = requests.get(url, params=params).json()
    ret = ''
    if weather != '':
        conditions = weather['days'][0]["conditions"]
        tempmax = weather['days'][0]["tempmax"]
        tempmin = weather['days'][0]["tempmin"]
        feelslike = weather['days'][0]["feelslike"]
        ret = '明天' + conditions + '，体感温度: ' + str(feelslike) + '℃\n' + '全天气温：' + str(tempmin) + '℃ ~ ' + str(tempmax) + '℃ ' 
    print("天气:", ret)
    return ret