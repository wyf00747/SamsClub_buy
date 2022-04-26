# -*- coding: UTF-8 -*-
# __author__ = 'guyongzx'
# __date__ = '2022-04-17'

import json
import requests
from time import sleep
import random

# 填写个人信息

deviceid = 'dd1d8100e555578bbed2c33d022316715a02'
authtoken = 'x'
deliveryType = '2'  # 1：极速达 2：全城配送
cartDeliveryType = 2  # 1：极速达 2：全城配送


# ## init config over ###

def getAmount(goodlist):
    global amount
    myUrl = 'https://api-sams.walmartmobile.cn/api/v1/sams/trade/settlement/getSettleInfo'
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
        "goodsList": goodlist,
        "uid": uid,
        "addressId": addressList_item.get('addressId'),
        "deliveryInfoVO": {
            "storeDeliveryTemplateId": good_store.get('storeDeliveryTemplateId'),
            "deliveryModeId": good_store.get('deliveryModeId'),
            "storeType": good_store.get('storeType')
        },
        "cartDeliveryType": cartDeliveryType,
        "storeInfo": {
            "storeId": good_store.get('storeId'),
            "storeType": good_store.get('storeType'),
            "areaBlockId": good_store.get('areaBlockId')
        },
        "couponList": [],
        "isSelfPickup": 0,
        "floorId": 1,
    }

    try:
        requests.packages.urllib3.disable_warnings()
        ret = requests.post(url=myUrl, headers=headers, data=json.dumps(data), verify=False)
        myRet = json.loads(ret.text)
        amount = ''
        if myRet['success']:
            amount = myRet['data'].get('totalAmount')
            return True, amount
        else:
            print('getAmount [Error]:')
            print(myRet)
            exit()
    except Exception as e:
        print('getAmount [Error]: ' + str(e))
        exit()


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
        return storeList_item, uid

    except Exception as e:
        print('getRecommendStoreListByLocation [Error]: ' + str(e))
        return False


def getUserCart(addressList, storeList, uid):
    global goodlist
    global isGo
    # amount目测可以随便写一个
    amount = "93320"
    myUrl = 'https://api-sams.walmartmobile.cn/api/v1/sams/trade/cart/getUserCart'
    data = {
        "uid": uid, "deliveryType": deliveryType, "deviceType": "ios", "storeList": storeList, "parentDeliveryType": 1,
        "homePagelongitude": addressList.get('longitude'), "homePagelatitude": addressList.get('latitude')
    }
    headers = {
        'Host': 'api-sams.walmartmobile.cn',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'Content-Type': 'application/json;charset=UTF-8',
        'Content-Length': '704',
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
    try:
        requests.packages.urllib3.disable_warnings()
        ret = requests.post(url=myUrl, headers=headers, data=json.dumps(data), verify=False)
        # print(ret.text)
        myRet = ret.json()
        if myRet['success']:
            normalGoodsList = (myRet['data'].get('floorInfoList')[0].get('normalGoodsList'))
            # time_list = myRet['data'].get('capcityResponseList')[0].get('list')
            for i in range(0, len(normalGoodsList)):
                spuId = normalGoodsList[i].get('spuId')
                storeId = normalGoodsList[i].get('storeId')
                quantity = normalGoodsList[i].get('quantity')
                goodsName = normalGoodsList[i].get('goodsName')
                stockQuantity = normalGoodsList[i].get('stockQuantity')
                goodlistitem = {
                    "spuId": spuId,
                    "storeId": storeId,
                    "isSelected": True,
                    "quantity": quantity,
                    "goodsName": goodsName,
                    "stockQuantity": stockQuantity
                }
                # print('目前有库存：' + 'squId' + str(spuId) + str(normalGoodsList[i].get('goodsName')) + '\t#数量：' + str(quantity) + '\t#金额：' + str(int(normalGoodsList[i].get('price')) / 100) + '元')
                goodlist.append(goodlistitem)

            # print(json.dumps(goodlist, sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False))
            # print(json.dumps(goodlist, ensure_ascii=False))

            fw = open('file/goodlist.txt', 'w')
            fw.write(str(json.dumps(goodlist, sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False)))
            fw.close()

            print('在file/goodlist.txt编辑商品后回车,如不编辑直接回车')
            s = str(input())
            fr = open('file/goodlist.txt','r')
            goodlist = json.loads(fr.read())
            fr.close()
            print('编辑后商品:')
            print(json.dumps(goodlist, sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False))
            for selectGood in goodlist:
                del selectGood['goodsName']
                del selectGood['stockQuantity']

            data = {"goodsList": goodlist,
                    "invoiceInfo": {},
                    "cartDeliveryType": cartDeliveryType, "floorId": 1, "amount": amount, "purchaserName": "",
                    "settleDeliveryInfo": {"expectArrivalTime": "startRealTime", "expectArrivalEndTime": "endRealTime",
                                           "deliveryType": deliveryType}, "tradeType": "APP", "purchaserId": "", "payType": 0,
                    "currency": "CNY", "channel": "wechat", "shortageId": 1, "isSelfPickup": 0, "orderType": 0,
                    "uid": uid, "appId": "wx57364320cb03dfba", "addressId": addressList_item.get('addressId'),
                    "deliveryInfoVO": {"storeDeliveryTemplateId": good_store.get('storeDeliveryTemplateId'),
                                       "deliveryModeId": good_store.get('deliveryModeId'),
                                       "storeType": good_store.get('storeType')}, "remark": "",
                    "storeInfo": {"storeId": good_store.get('storeId'), "storeType": good_store.get('storeType'),
                                  "areaBlockId": good_store.get('areaBlockId')},
                    "shortageDesc": "其他商品继续配送（缺货商品直接退款）", "payMethodId": "1486659732"}
            # print(json.dumps(data, sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False))
            fdata = open('file/data.txt','w')
            fdata.write(str(json.dumps(data, sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False)))
            fdata.close()

            headers = {
                'Host': 'api-sams.walmartmobile.cn',
                'Connection': 'keep-alive',
                'Accept': '*/*',
                'Content-Type': 'application/json',
                'Content-Length': '1617',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'User-Agent': 'SamClub/5.0.45 (iPhone; iOS 15.4; Scale/3.00)',
                'device-name': 'iPhone14,3',
                'device-os-version': '15.4',
                'device-id': deviceid,
                'longitude': address.get('longitude'),
                'latitude': address.get('latitude'),
                'device-type': 'ios',
                'auth-token': authtoken,
                'app-version': '5.0.45.1'
            }

            fheaders = open('file/headers.txt','w')
            fheaders.write(str(json.dumps(headers, sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False)))
            fheaders.close()
            isGo = False
            print("购物车加载完成,运行order.py")
        else:
            print("购物车查询接口繁忙,等待重试")
    except Exception as e:
        print('getUserCart [Error]: ' + str(e))

def init():
    address = address_list()
    store, uid = getRecommendStoreListByLocation(address.get('latitude'), address.get('longitude'))
    return address, store, uid


if __name__ == '__main__':
    thCount = 1
    count = 0
    isGo = True
    deliveryTime = []
    goodlist = []
    # 初始化,应该不需要做重试处理
    address, store, uid = init()
    # 获取购物车信息,高峰期需要重试
    while isGo:
        getUserCart(address, store, uid)
        sleep_time = random.randint(1, 2)
        sleep(sleep_time)

