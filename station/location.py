# -*- coding: UTF-8 -*-
# __author__ = 'guyong'
# __date__ = '2022-04-17'

import json
import requests
from time import sleep
import datetime

authToken = ""

def getRecommendStoreListByLocation(longitude, latitude):
    print(str(longitude) + ", " + str(latitude))

    global storeList_item
    myUrl = 'https://api-sams.walmartmobile.cn/api/v1/sams/merchant/storeApi/getRecommendStoreListByLocation'
    data = {
        'longitude': longitude,
        'latitude': latitude
    }
    headers = {
        'Host': 'api-sams.walmartmobile.cn',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'Content-Type': 'application/json;charset=UTF-8',
        'Content-Length': '45',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'SamClub/5.0.45 (iPhone; iOS 15.4; Scale/3.00)',
        'device-name': 'iPhone14,3',
        'device-os-version': '15.4',
        'device-type': 'ios',
        'auth-token': authToken,
        'app-version': '5.0.45.1'
    }
    requests.packages.urllib3.disable_warnings()
    ret = requests.post(url=myUrl, headers=headers, data=json.dumps(data), verify=False)
    myRet = ret.json()
    # print(ret.text)
    if not myRet['success']:
        return
    else:
        storeList = myRet['data'].get('storeList')
        for i in range(0, len(storeList)):
            if storeList[i].get("storeId") != '9991' and storeList[i].get("storeId") != '9996':
                key = str(storeList[i].get("storeId")) + "==" + str(storeList[i]['storeRecmdDeliveryTemplateData']['storeDeliveryTemplateId']) + "--" + str(storeList[i].get("storeName"))
                print(key)

                # 加入performanceTemplateName
                performanceTemplateName = getDeliveryInfo(str(storeList[i]['storeRecmdDeliveryTemplateData']['storeDeliveryTemplateId']))
                print(performanceTemplateName)
                storeList_item[key] = "performanceTemplateName: " + str(performanceTemplateName) + " storeType: " + str(storeList[i].get("storeType")) + " storeId: " + str(storeList[i].get("storeId")) + " areaBlockId: " + str(storeList[i].get('storeAreaBlockVerifyData').get("areaBlockId")) + " deliveryModeId:" + str(storeList[i].get('storeDeliveryModeVerifyData').get("deliveryModeId"))
                # storeList_item[key] = {
                #     'performanceTemplateName': performanceTemplateName,
                #     'storeType': storeList[i].get("storeType"),
                #     'storeId': storeList[i].get("storeId"),
                #     'areaBlockId': storeList[i].get('storeAreaBlockVerifyData').get("areaBlockId"),
                #     'storeDeliveryTemplateId': storeList[i].get('storeRecmdDeliveryTemplateData').get(
                #         "storeDeliveryTemplateId"),
                #     'deliveryModeId': storeList[i].get('storeDeliveryModeVerifyData').get("deliveryModeId"),
                #     'storeName': storeList[i].get("storeName")
                # }
                fw.write(str(longitude) + ", " + str(latitude) + " " + key + ":" + storeList_item[key] + "\n")

def getDeliveryInfo(storeDeliveryTemplateId):
    myUrl = 'https://api-sams.walmartmobile.cn/api/v1/sams/delivery/portal/getCapacityData'
    headers = {
        'Host': 'api-sams.walmartmobile.cn',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'Content-Type': 'application/json;charset=UTF-8',
        'Content-Length': '45',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'SamClub/5.0.45 (iPhone; iOS 15.4; Scale/3.00)',
        'device-name': 'iPhone14,3',
        'device-os-version': '15.4',
        'device-type': 'ios',
        'auth-token': authToken,
        'app-version': '5.0.45.1'
    }

    data = {
        "perDateList": date_list,
        "storeDeliveryTemplateId": storeDeliveryTemplateId
    }
    try:
        requests.packages.urllib3.disable_warnings()
        ret = requests.post(url=myUrl, headers=headers, data=json.dumps(data), verify=False)
        myRet = ret.json()
        if not myRet['success']:
            return "fail"
        else:
            return myRet['data']['getPortalPerformanceTemplateResponse']['performanceTemplateName']

    except Exception as e:
        print('getCapacityData [Error]: ' + str(e))

# getRecommendStoreListByLocation(121,31)
storeList_item = {}
longStart = 12104
longEnd = 12194

laStart = 3090
laEnd = 3142

# 查询配送信息的一周动态组装
date_list = []
for i in range(0, 7):
    date_list.append((datetime.datetime.now() + datetime.timedelta(days=i)).strftime('%Y-%m-%d'))

fw = open('log.txt', 'w')

# 步进默认6,需要细致的可以往小了调
for long in range(longStart, longEnd, 5):
    long = long / 100
    for la in range(laStart, laEnd, 5):
        la = la / 100
        getRecommendStoreListByLocation(long, la)
        sleep(0.5)
fw.close()

fw = open('list.txt', 'w')
for k, v in storeList_item.items():
    fw.write(k + ":" + v + "\n")
fw.close()

