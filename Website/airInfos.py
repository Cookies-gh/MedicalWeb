# -*- coding:UTF-8 -*-
from suds.client import Client
from db_method import insert


#获取天气信息，result_dict是一个字典，key是地点名,value是一个字典，包含着一个地点的污染物信息   编码为utf-8
#样例：
#'\xe6\x98\x8c\xe5\xb9\xb3':{'Station': '\xe6\x98\x8c\xe5\xb9\xb3', 'Date_Time': '2017-05-10 20:00:00', 'CO': '0.6', 'PM10': '101', 'PM2.5': '34', 'O3': '163', 'NO2': '15'}

def pp():
    print "aaa!"

def getAirInfo():
    print "getAirInfo"
    AirType = ['CO','O3','PM2.5','PM10','SO2','NO2']
    url = 'http://mobile.bjmemc.com.cn/AirService/Service.asmx?wsdl'
    client = Client(url)

    header = client.factory.create('MySoapHeader')
    header.UserName = 'beijingaqi'
    header.PassWord = 'bjaqi2012pds'
    client.set_options(soapheaders=[header,])

    result = client.service.GetData()
    # print result

    # js = json.dumps(result)
    result = result[10:len(result)-2]
    result = result.replace('{','')
    result = result.replace('"','')
    list = result.split('}')
    del list[len(list) - 1]
    result_dict = {}
    i = 0
    tempDict = {}
    # print len(list)
    for item in list:
        if(item[0] == ','):
            item = item[1:]
        # print item
        list_1 = item.split(',',4)
        del list_1[len(list_1) - 1]

        #tempDict为空
        # print tempDict
        if 'Station' not in tempDict:
            list_2 = list_1[0].split(':', 1)
            tempDict[list_2[0].encode("utf-8")] = list_2[1].encode("utf-8")
            list_2 = list_1[1].split(':', 1)
            tempDict[list_2[0].encode("utf-8")] = list_2[1].encode("utf-8")

        if list_1[1].split(':', 1)[1].encode("utf-8") == tempDict['Station']:
            list_2 = list_1[2].split(':', 1)
            tempDict[list_2[1].encode("utf-8")] = list_1[3].split(':', 1)[1].encode("utf-8")
        else:
            result_dict[tempDict['Station']] = tempDict
            tempDict = {}
            list_2 = list_1[0].split(':', 1)
            tempDict[list_2[0].encode("utf-8")] = list_2[1].encode("utf-8")
            list_2 = list_1[1].split(':', 1)
            tempDict[list_2[0].encode("utf-8")] = list_2[1].encode("utf-8")
            list_2 = list_1[2].split(':', 1)
            tempDict[list_2[1].encode("utf-8")] = list_1[3].split(':', 1)[1].encode("utf-8")
    result_dict[tempDict['Station']] = tempDict
    # print len(result_dict)
    for i in result_dict:
        if len(result_dict[i]) < 8:
            for key in AirType:
                if key not in result_dict[i]:
                    result_dict[i][key] = '未公布'
    # print result_dict
    return insert.addAirInfo(result_dict)
# print "aaa"


