# -*- coding: UTF-8 -*-
# __author__ = 'guyongzx'
# __date__ = '2022-04-17'

import json
import requests
from time import sleep
import random
import datetime
import threading

# 填写个人信息

deviceid = 'dd1d8100e555578bbed2c33d022316715a02'
authtoken = 'x'
# 改为自己的barkid
barkId = "x"
deliveryType = 2  # 1：极速达 2：全城配送
cartDeliveryType = 2  # 1：极速达 2：全城配送


def address_list():
    global addressList_item
    print('###初始化地址')
    myUrl = 'https://api-sams.walmartmobile.cn/api/v1/sams/sams-user/receiver_address/address_list'
    headers = {
        'Host': 'api-sams.walmartmobile.cn',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'SamClub/5.0.45 (iPhone; iOS 15.4; Scale/3.00)',
        'device-name': 'iPhone14,3',
        'device-os-version': '15.4',
        'device-id': deviceid,
        'device-type': 'ios',
        'auth-token': authtoken,
        'app-version': '5.0.45.1'
    }
    requests.packages.urllib3.disable_warnings()
    ret = requests.get(url=myUrl, headers=headers, verify=False)
    myRet = ret.json()
    addressList = myRet['data'].get('addressList')
    addressList_item = []

    for i in range(0, len(addressList)):
        addressList_item.append({
            'addressId': addressList[i].get("addressId"),
            'mobile': addressList[i].get("mobile"),
            'name': addressList[i].get("name"),
            'countryName': addressList[i].get('countryName'),
            'provinceName': addressList[i].get('provinceName'),
            'cityName': addressList[i].get('cityName'),
            'districtName': addressList[i].get('districtName'),
            'receiverAddress': addressList[i].get('receiverAddress'),
            'detailAddress': addressList[i].get('detailAddress'),
            'latitude': addressList[i].get('latitude'),
            'longitude': addressList[i].get('longitude')
        })
        print('[' + str(i) + ']' + str(addressList[i].get("name")) + str(addressList[i].get("mobile")) + str(addressList[i].get(
            "districtName")) + str(addressList[i].get("receiverAddress")) + str(addressList[i].get("detailAddress")))
    print('根据编号选择地址:')
    s = int(input())
    addressList_item = addressList_item[s]
    # print(addressList_item)
    return addressList_item


def getRecommendStoreListByLocation(latitude, longitude):
    global uid
    global good_store

    storeList_item = []
    print('###初始化商店')
    myUrl = 'https://api-sams.walmartmobile.cn/api/v1/sams/merchant/storeApi/getRecommendStoreListByLocation'
    data = {
        'longitude': longitude,
        'latitude': latitude}
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
        'device-id': deviceid,
        'latitude': latitude,
        'device-type': 'ios',
        'auth-token': authtoken,
        'app-version': '5.0.45.1'
    }
    try:
        requests.packages.urllib3.disable_warnings()
        ret = requests.post(url=myUrl, headers=headers, data=json.dumps(data), verify=False)
        myRet = ret.json()
        storeList = myRet['data'].get('storeList')
        for i in range(0, len(storeList)):
            storeList_item.append(
                {
                    'storeType': storeList[i].get("storeType"),
                    'storeId': storeList[i].get("storeId"),
                    'areaBlockId': storeList[i].get('storeAreaBlockVerifyData').get("areaBlockId"),
                    'storeDeliveryTemplateId': storeList[i].get('storeRecmdDeliveryTemplateData').get(
                        "storeDeliveryTemplateId"),
                    'deliveryModeId': storeList[i].get('storeDeliveryModeVerifyData').get("deliveryModeId"),
                    'storeName': storeList[i].get("storeName")
                })
            print('[' + str(i) + ']' + str(storeList_item[i].get("storeId")) + str(storeList_item[i].get("storeName")))
        print('根据编号下单商店:')
        s = int(input())
        good_store = storeList_item[s]
        uidUrl = 'https://api-sams.walmartmobile.cn/api/v1/sams/sams-user/user/personal_center_info'
        requests.packages.urllib3.disable_warnings()
        ret = requests.get(url=uidUrl, headers={
            'Host': 'api-sams.walmartmobile.cn',
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': 'SamClub/5.0.45 (iPhone; iOS 15.4; Scale/3.00)',
            'device-name': 'iPhone14,3',
            'device-os-version': '15.4',
            'device-id': deviceid,
            'latitude': latitude,
            'device-type': 'ios',
            'auth-token': authtoken,
            'app-version': '5.0.45.1'
        }, verify=False)
        # print(ret.text)
        uidRet = json.loads(ret.text)
        uid = uidRet['data']['memInfo']['uid']
        return good_store, uid

    except Exception as e:
        print('getRecommendStoreListByLocation [Error]: ' + str(e))
        return False

def getBaoGongInfo(uid, address):
    global goodlist
    myUrl = 'https://api-sams.walmartmobile.cn/api/v1/sams/decoration/portal/show/getPageData'
    data = {
        "uid": uid,
        "pageContentId": "1187641882302384150",
        "addressInfo": {
            "provinceCode": "",
            "receiverAddress": address['detailAddress'],
            "districtCode": "",
            "cityCode": ""
        },
        "authorize": True,
        "latitude": address.get('latitude'),
        "longitude": address.get('longitude')
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
        'device-id': deviceid,
        'latitude': address.get('latitude'),
        'device-type': 'ios',
        'auth-token': authtoken,
        'app-version': '5.0.45.1'
    }
    try:
        requests.packages.urllib3.disable_warnings()
        ret = requests.post(url=myUrl, headers=headers, data=json.dumps(data), verify=False)
        myRet = ret.json()
        if not myRet['success']:
            return
        else:
            for pageModuleVO in myRet['data']['pageModuleVOList']:
                if not 'goodsList' in pageModuleVO['renderContent']:
                    continue
                else:
                    goodsList = pageModuleVO['renderContent']['goodsList']
                    for good in goodsList:
                        if int(good['spuStockQuantity']) > 0:
                            if good['spuId'] not in goodlist:
                                print("有货!!! " + "名称:" + good['title'] + " 详情:" + good['subTitle'])
                                if addCart(uid, good):
                                    goodlist[str(good['spuId'])] = good
                                    # 此处可以加通知
                                    # notify()
                            else:
                                print("已加购..." + "名称:" + good['title'] + " 详情:" + good['subTitle'])
                        else:
                            print("无货... " + "名称:" + good['title'] + " 详情:" + good['subTitle'])
    except Exception as e:
        # print(myRet['data']['pageModuleVOList'])
        print('getBaoGongInfo [Error]: ' + str(e))

def addCart(uid, good):
    myUrl = 'https://api-sams.walmartmobile.cn/api/v1/sams/trade/cart/addCartGoodsInfo'
    data = {
        "uid": uid,
        "cartGoodsInfoList": [
            {
                "spuId": good['spuId'],
                "storeId": good['storeId'],
                "increaseQuantity": 1,
                "price": good['priceInfo'][0]['price'],
                "goodsName": good['title']
            }
        ]
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
        'device-id': deviceid,
        'latitude': address.get('latitude'),
        'device-type': 'ios',
        'auth-token': authtoken,
        'app-version': '5.0.45.1'
    }
    try:
        requests.packages.urllib3.disable_warnings()
        ret = requests.post(url=myUrl, headers=headers, data=json.dumps(data), verify=False)
        myRet = ret.json()
        if not myRet['success']:
            print("加入购物车失败... " + good['subTitle'])
            return False
        else:
            print("加入购物车成功!!! " + good['subTitle'])
            return True
    except Exception as e:
        print('addCart [Error]: ' + str(e))

def getCapacityData(good):
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
        'device-id': deviceid,
        'latitude': address.get('latitude'),
        'device-type': 'ios',
        'auth-token': authtoken,
        'app-version': '5.0.45.1'
    }
    data = {
        "perDateList": date_list,
        "storeDeliveryTemplateId": storeDeliveryTemplateId
    }
    try:
        requests.packages.urllib3.disable_warnings()
        ret = requests.post(url=myUrl, headers=headers, data=json.dumps(data), verify=False)
        # print(ret.text)
        myRet = ret.json()
        # print('#获取可用配送时间中')
        list1 = myRet['data']['capcityResponseList']
        for days in list1:
            for capcity in days['list']:
                if not capcity['timeISFull']:
                    print("有配送时间")
                    order(capcity['startRealTime'], capcity['endRealTime'], good)
                else:
                    print("无配送时间")
    except Exception as e:
        print('getCapacityData [Error]: ' + str(e))


def order(startTime, endTime, good):
    myUrl = 'https://api-sams.walmartmobile.cn/api/v1/sams/trade/settlement/commitPay'
    list = []
    order_good = {
        "spuId": good['spuId'],
        "storeId": good['storeId'],
        "isSelected": True,
        "quantity": 1
    }
    list.append(order_good)
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
        'device-id': deviceid,
        'latitude': address.get('latitude'),
        'longitude': address.get('longitude'),
        'device-type': 'ios',
        'auth-token': authtoken,
        'app-version': '5.0.45.1'
    }
    data = {
        "goodsList": list,
        "invoiceInfo": {},
        "cartDeliveryType": cartDeliveryType, "floorId": 1, "amount": '66666', "purchaserName": "",
        "settleDeliveryInfo": {"expectArrivalTime": startTime, "expectArrivalEndTime": endTime,
                               "deliveryType": deliveryType}, "tradeType": "APP", "purchaserId": "", "payType": 0,
        "currency": "CNY", "channel": "wechat", "shortageId": 1, "isSelfPickup": 0, "orderType": 0,
        "uid": uid, "appId": "wx57364320cb03dfba", "addressId": address.get('addressId'),
        "deliveryInfoVO": {"storeDeliveryTemplateId": store.get('storeDeliveryTemplateId'),
                           "deliveryModeId": store.get('deliveryModeId'),
                           "storeType": store.get('storeType')}, "remark": "",
        "storeInfo": {"storeId": store.get('storeId'), "storeType": store.get('storeType'),
                      "areaBlockId": store.get('areaBlockId')},
        "shortageDesc": "其他商品继续配送（缺货商品直接退款）", "payMethodId": "1486659732"
    }
    # print(json.dumps(data))
    # print(global_headers)
    # print(body_data)
    try:
        requests.packages.urllib3.disable_warnings()
        ret = requests.post(url=myUrl, headers=headers, data=json.dumps(data), verify=False)
        # print(ret.text)
        myRet = ret.json()
        print(myRet['msg'])
        status = myRet.get('success')
        if status:
            print('【成功】哥，咱家有菜了~')
            # 通知自由发挥
            notify(good['subTitle'])
            exit()
    except Exception as e:
        print('order [Error]: ' + str(e))

# 加入bark通知 url地址改为自己的!!!
def notify(name):
    myUrl = "https://api.day.app/" + barkId + "/保供下单成功!!!/" + name
    try:
        requests.packages.urllib3.disable_warnings()
        requests.get(url=myUrl, verify=False)
    except Exception as e:
        print('notify [Error]: ' + str(e))

def init():
    address = address_list()
    store, uid = getRecommendStoreListByLocation(address.get('latitude'), address.get('longitude'))
    return address, store, uid

def runCreateOrder():
    global goodlist
    while 1:
        if len(goodlist) > 0 and len(threadPool) < len(goodlist):
            for k, v in goodlist.items():
                if str(v['spuId']) not in threadPool:
                    print("启动下单进程: " + v['title'])
                    tOrder = threading.Thread(target=runOrder,args=(v, ))
                    tOrder.start()
                    threadPool[str(v['spuId'])] = "start"

        sleep(1)

def runOrder(good):
    while 1:
        getCapacityData(good)
        sleep_time = random.randint(1000, 2000) / 1000
        sleep(sleep_time)

def runGetBaogongInfo():

    while 1:
        getBaoGongInfo(uid, address)
        sleep_time = random.randint(2000, 10000) / 1000
        sleep(sleep_time)

if __name__ == '__main__':
    goodlist = {}
    # 下单线程池
    threadPool = {}
    date_list = []
    for i in range(0, 7):
        date_list.append((datetime.datetime.now() + datetime.timedelta(days=i)).strftime('%Y-%m-%d'))

    # 初始化,应该不需要做重试处理
    address, store, uid = init()
    print(store)
    # 设定下getCapacityData的头信息
    storeDeliveryTemplateId = store['storeDeliveryTemplateId']

    t1 = threading.Thread(target=runGetBaogongInfo, args=())
    t1.start()

    t2 = threading.Thread(target=runCreateOrder, args=())
    t2.start()