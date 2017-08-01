# -*- coding:UTF-8 -*-
import urllib2
import json
from db_method import insert
import datetime

def getWeatherInfo():
    print "getWeatherInfo"
    citys = ['北京','海淀','朝阳','顺义','怀柔','通州','昌平','延庆','丰台','石景山','大兴','房山','密云','门头沟','平谷','东城','西城']
    citys_pinyin = ['haidian','chaoyang','shunyi','huairou','tongzhou','changping','yanqing','fengtai','shijingshan','daxing','fangshan','miyun','mentougou','pinggu','dongcheng','xicheng']
    key = '34f5508c1359420f87fcba0c27b366af'
    #7b2a60a1e88c4fab967aea95cfc5efa7
    for city in citys:
        url = "https://free-api.heweather.com/v5/weather?city="+ city +"&key=" + key
        response = urllib2.urlopen(url)
        result = (json.load(response))['HeWeather5'][0]
        # print result
        if 'aqi' in result:
            aqi_t = result['aqi']['city']
        else:
            aqi_t = {'aqi':-1,'pm10':-1,'pm25':-1,'qlty':"-1"}
        # aqi_t = result['aqi']['city']
        tmp = result['daily_forecast'][0]['tmp']
        wind = result['daily_forecast'][0]['wind']

        date = result['daily_forecast'][0]['date']

        city = result['basic']['city']

        aqi = int(aqi_t['aqi'])
        if 'co' in aqi_t:
            co = int(aqi_t['co'])
        else:
            co = -1
        if 'no2' in aqi_t:
            no2 = int(aqi_t['no2'])
        else:
            no2 = -1
        if 'o3' in aqi_t:
            o3 = int(aqi_t['o3'])
        else:
            o3 = -1
        if 'so2' in aqi_t:
            so2 = int(aqi_t['so2'])
        else:
            so2 = -1
        pm10 = int(aqi_t['pm10'])
        pm25 = int(aqi_t['pm25'])
        qlty = aqi_t['qlty']
        #天气状况 白天 晚上
        txt_d = result['daily_forecast'][0]['cond']['txt_d']
        txt_n = result['daily_forecast'][0]['cond']['txt_n']
        #湿度
        hum = int(result['daily_forecast'][0]['hum']) # 湿度
        #温度
        tmp_max = int(tmp['max'])
        tmp_min = int(tmp['min'])
        #风
        wind_deg = wind['deg']
        wind_dir =  wind['dir']
        wind_sc =  wind['sc']
        wind_spd =  wind['spd']
        data = [datetime.datetime.strptime(date, "%Y-%m-%d").date(), city, aqi, co, no2, o3, pm10, pm25, qlty, so2, txt_d,
                txt_n, hum, tmp_max, tmp_min, wind_deg, wind_dir, wind_sc, wind_spd]
        # print data, type(data), data[0]
        insert.addWeatherInfo(data)



