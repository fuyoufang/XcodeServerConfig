#!/usr/bin/env python3

import json
import requests
from requests_toolbelt import MultipartEncoder
import time
import hmac
import hashlib
import base64
import urllib.parse
import sys, getopt
import DingTalk
import getopt
import SourceControl

# **********************需要填的信息**************************

#蒲公英
pgy_uKey = ""
pgy_api_key = ""
pgy_Url="https://upload.pgyer.com/apiv1/app/upload"

# 手机号
one_phone = '16666666666' # 
two_phone ='16666666666' # 
three_phone = '16666666666' # 
four_phone ='16666666666' # 
five_phone ='16666666666' # 


def notification_upload_pgy_error(xcs, info):
    text = '# [流泪]iOS 包上传蒲公英失败[流泪] \n'
    text += '\n--------\n'
    text += '请解决 @{0} \n'.format(five_phone)
    text += 'XcodeServer 地址 vnc://172.16.1.150 \n'
    text += '\n--------\n'
    text += '错误信息： \n'
    text += '> {0}'.format(info)

    data = {
        "msgtype": "markdown",
        "markdown": {
            "title":"[流泪][流泪] iOS 上传蒲公英失败了",
            "text": text
        },
        "at": {
          "atMobiles": [
              five_phone
          ],
          "isAtAll": False
      }
    }
    r = requests.post(url=DingTalk.getDingTalkRbootUrl(), json=data)

def notification_upload_pgy_success(xcs, info):
    infoData = info.get("data")
    text = '# [鼓掌]iOS 最近版本上传蒲公英成功[鼓掌] \n'
    
    text += '\n--------\n'
    text += '### 编译信息 \n'
    text += '- **编译结果**：{0} \n'.format(xcs.get('XCS_INTEGRATION_RESULT'))
    text += '- **错误总数**：{0} \n'.format(xcs.get('XCS_ERROR_COUNT'))
    XCS_ERROR_CHANGE = int(xcs.get('XCS_ERROR_CHANGE', "0"))
    if XCS_ERROR_CHANGE > 0:
        text += '> 比上次「增加」了：{0} \n'.format(XCS_ERROR_CHANGE)
    elif XCS_ERROR_CHANGE < 0:
        text += '> 比上次「减少」了：{0} \n'.format(-XCS_ERROR_CHANGE)
    else:
        text += '> 和上次「一样」\n'

    text += '- **警告总数**：{0} \n'.format(xcs.get('XCS_WARNING_COUNT'))
    XCS_WARNING_CHANGE = int(xcs.get('XCS_WARNING_CHANGE', "0"))
    if XCS_WARNING_CHANGE > 0:
        text += '> 比上次「增加」了：{0} \n'.format(XCS_WARNING_CHANGE)
    elif XCS_WARNING_CHANGE < 0:
        text += '> 比上次「减少」了：{0} \n'.format(-XCS_WARNING_CHANGE)
    else:
        text += '> 和上次「一样」\n'

    text += '- **静态分析警告总数**：{0} \n'.format(xcs.get('XCS_ANALYZER_WARNING_COUNT'))
    XCS_ANALYZER_WARNING_CHANGE = int(xcs.get('XCS_ANALYZER_WARNING_CHANGE', "0"))
    if XCS_ANALYZER_WARNING_CHANGE > 0:
        text += '> 比上次「增加」了：{0} \n'.format(XCS_ANALYZER_WARNING_CHANGE)
    elif XCS_ANALYZER_WARNING_CHANGE < 0:
        text += '> 比上次「减少」了：{0} \n'.format(-XCS_ANALYZER_WARNING_CHANGE)
    else:
        text += '> 和上次「一样」\n'

    text += '- **执行的测试总数**：{0} \n'.format(xcs.get('XCS_TESTS_COUNT'))
    XCS_TESTS_CHANGE = int(xcs.get("XCS_TESTS_CHANGE", "0"))
    if  XCS_TESTS_CHANGE > 0:
        text += '> 比上次「增加」了：{0} \n'.format(XCS_TESTS_CHANGE)
    elif XCS_TESTS_CHANGE < 0:
        text += '> 比上次「减少」了：{0} \n'.format(XCS_TESTS_CHANGE)
    else:
        text += '> 和上次「一样」\n'


    ## 版本信息： 
    text += '\n--------\n'
    text += '### 版本信息 \n'
    text += '- **名称**：{0} \n'.format(infoData.get('appName'))
    text += '- **App大小**：{0} MB\n'.format(int(int(infoData.get('appFileSize')) / 1024 / 1024))
    text += '- **版本**：{0} \n'.format(infoData.get('appVersion'))
    text += '- **版本No**：{0} \n'.format(infoData.get('appVersionNo'))
    text += '- **BuildVersion**：{0} \n'.format(infoData.get('appBuildVersion'))
    #text += '- **appIdentifier**: {0} \n'.format(infoData.get('appIdentifier'))
    text += '- **创建时间**：{0} \n'.format(infoData.get('appCreated'))
    text += '- **上传时间**：{0} \n'.format(infoData.get('appUpdated'))
    # text += '- **appQRCodeURL**: {0} '.format(infoData.get('appQRCodeURL'))
    text += '- **短连接**：https://www.pgyer.com/{0} \n'.format(infoData.get('appShortcutUrl'))
    text += '- **本地下载二维码** \n'
    text += '![code]({}) \n'.format(infoData.get('appQRCodeURL'))

    ## Git信息： 
    text += '\n--------\n'
    text += '### 代码变更信息 \n'
    
    if 'XCS_OUTPUT_DIR' in xcs:
        log_dir= xcs['XCS_OUTPUT_DIR'] + "/sourceControl.log"
        project_dir = xcs['XCS_PRIMARY_REPO_DIR'] #+ "/LoveHottie"
        print("工程路径是："+project_dir)
        commits = SourceControl.getCommits(log_dir, project_dir)
        if commits is not None and len(commits) > 0:
            for c in commits:
                # print(c.hexsha)
                text += '- [{}] {}\n'.format(c.author, c.message)
        else:    
            text += '暂未代码变更信息 \n'        
    else:
        text += '暂未代码变更信息 \n'
    
    text += '\n--------\n'
    text += '\n\n请注意查收：@{} @{} @{} @{} [送花花][送花花]'.format(
        one_phone,
        two_phone,
        three_phone,
        four_phone,)

    print(text)
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title":"xcodeserver 上传蒲公英成功",
            "text": text
        },
        "at": {
          "atMobiles": [
                one_phone,
                two_phone,
                three_phone,
                four_phone
          ],
          "isAtAll": False
      }
    }
    r = requests.post(url=DingTalk.getDingTalkRbootUrl(), json=data)
    print(r.text)

# 提交蒲公英
# 文档地址： https://www.pgyer.com/doc/api#uploadApp
def upload_pgy(file):
    # return '{"code":0,"message":"","data":{"appKey":"6cb2f6df323df98f18dca580fde6fb7b","userKey":"4688f2ce3a6092b231e9121099f81b16","appType":"1","appIsLastest":"1","appFileSize":"106846852","appName":"LoveHottie","appVersion":"1.0.0","appVersionNo":"2021010501","appBuildVersion":"6","appIdentifier":"com.zoneyet.lovehottie","appIcon":"6a79646af2742b83dea090c80b7b6e8e","appDescription":"","appUpdateDescription":"","appScreenshots":"","appShortcutUrl":"r5nQ","appCreated":"2021-01-06 16:07:58","appUpdated":"2021-01-06 16:07:58","appQRCodeURL":"https:\/\/www.pgyer.com\/app\/qrcodeHistory\/302e509d53a3bfa05aac40e50be579aa74fa2ddeb5141a9e32bc7500b3101e45"}}'
    # return '{"code":200,"message":"_api_key could not be empty"}'
    m = MultipartEncoder(
        fields={
            'uKey': pgy_uKey, 
            '_api_key': pgy_api_key,
            'file': ('GaGaHi.ipa', open(file, 'rb'), '')
            }
        )

    r = requests.post(url=pgy_Url, data=m, headers={'Content-Type': m.content_type})
    r.encoding='utf-8'
    return r.text
    
def main(argv):
    # 
    # XCS_INTEGRATION_RESULT = '' # 表示集成结果的字符串，例如， 成功、 测试失败、 构建错误、 和 取消集成。 这些变量用于后集成触发器。
    # XCS_SOURCE_DIR = '' # Xcode Server包含源码仓库的顶级目录。对于存储库本身的路径，
    # XCS_PRODUCT = '' # .app、 .ipa、 或 .package 文件路径（如果集成期间从归档中输出了产品的话）。
    # XCS_ERROR_COUNT = '' # 集成期间产生的错误总数
    # XCS_ERROR_CHANGE = '' # 相对于上次集成产生的错误数值的改变。该值可以为负。
    # XCS_WARNING_COUNT = '' # 集成期间产生的警告总数。
    # XCS_WARNING_CHANGE = '' # 相对于上次集成产生的警告数值的改变。该值可以为负。
    # XCS_ANALYZER_WARNING_COUNT = '' # 集成期间产生的静态分析警告总数。
    # XCS_ANALYZER_WARNING_CHANGE = '' # 相对于上次集成产生的静态分析警告数值的改变。该值可以为负。
    # XCS_TEST_FAILURE_COUNT = '' # 集成期间产生的测试失败总数。
    # XCS_TEST_FAILURE_CHANGE = '' # 相对于上次集成产生的测试失败数值的改变。该值可以为负。
    # XCS_TESTS_COUNT = '' # 集成执行的测试总数。
    # XCS_TESTS_CHANGE = '' # 相对于上次集成执行的测试数值的改变。该值可以为负。

    print(argv)

    # 打包信息
    xcs = {}
    try:
        opts, args = getopt.getopt(argv, "", [
            "XCS_INTEGRATION_RESULT=", 
            "XCS_SOURCE_DIR=", 
            "XCS_PRODUCT=",
            "XCS_ERROR_COUNT=",
            "XCS_ERROR_CHANGE=",
            "XCS_WARNING_COUNT=",
            "XCS_WARNING_CHANGE=",
            "XCS_ANALYZER_WARNING_COUNT=",
            "XCS_ANALYZER_WARNING_CHANGE=",
            "XCS_TEST_FAILURE_COUNT=",
            "XCS_TEST_FAILURE_CHANGE=",
            "XCS_TESTS_COUNT=",
            "XCS_TESTS_CHANGE=",
            "XCS_OUTPUT_DIR=",
            "XCS_PRIMARY_REPO_DIR="
        ])
    except getopt.GetoptError as error:
        print(error)
        print('Error: xcodeserver.py --XCS_INTEGRATION_RESULT <XCS_INTEGRATION_RESULT> --XCS_SOURCE_DIR <XCS_SOURCE_DIR>')
        notification_upload_pgy_error(xcs, "打包结果参数异常")

        sys.exit(2)

    # 处理 返回值options是以元组为元素的列表。
    for opt, arg in opts:
        if opt in ("--XCS_INTEGRATION_RESULT"):
            xcs['XCS_INTEGRATION_RESULT'] = arg    
        elif opt in ("--XCS_SOURCE_DIR"):
            xcs['XCS_SOURCE_DIR'] = arg
        elif opt in ("--XCS_PRODUCT"):
            xcs['XCS_PRODUCT'] = arg
        elif opt in ("--XCS_ERROR_COUNT"):
            xcs['XCS_ERROR_COUNT'] = arg
        elif opt in ("--XCS_ERROR_CHANGE"):
            xcs['XCS_ERROR_CHANGE'] = arg
        elif opt in ("--XCS_WARNING_COUNT"):
            xcs['XCS_WARNING_COUNT'] = arg
        elif opt in ("--XCS_WARNING_CHANGE"):
            xcs['XCS_WARNING_CHANGE'] = arg
        elif opt in ("--XCS_ANALYZER_WARNING_COUNT"):
            xcs['XCS_ANALYZER_WARNING_COUNT'] = arg
        elif opt in ("--XCS_ANALYZER_WARNING_CHANGE"):
            xcs['XCS_ANALYZER_WARNING_CHANGE'] = arg
        elif opt in ('--XCS_TEST_FAILURE_COUNT'):
            xcs['XCS_TEST_FAILURE_COUNT'] = arg
        elif opt in ('--XCS_TEST_FAILURE_CHANGE'):
            xcs['XCS_TEST_FAILURE_CHANGE'] = arg
        elif opt in ('--XCS_TESTS_COUNT'):
            xcs['XCS_TESTS_COUNT'] = arg
        elif opt in ('--XCS_TESTS_CHANGE'):
            xcs['XCS_TESTS_CHANGE'] = arg
        elif opt in ('--XCS_OUTPUT_DIR'):
            xcs['XCS_OUTPUT_DIR'] = arg
        elif opt in ('--XCS_PRIMARY_REPO_DIR'):
            xcs['XCS_PRIMARY_REPO_DIR'] = arg

            

    
    if 'XCS_PRODUCT' not in xcs:
        print('请提供 --XCS_PRODUCT 参数，即 ipa 的路径')
        notification_upload_pgy_error(xcs, "打包结果参数异常")
        sys.exit(2)

    print('xcs参数信息')
    print(xcs)

    XCS_PRODUCT = xcs['XCS_PRODUCT']
    print('ipa 路径:{}'.format(XCS_PRODUCT))
    text = upload_pgy(XCS_PRODUCT)
    upload_result = json.loads(text)
    code= int(upload_result.get('code'))
    print(code) 

    if (code != 0):
        print('上传失败')
        notification_upload_pgy_error(xcs, upload_result)
    else:
        notification_upload_pgy_success(xcs, upload_result)


if __name__ == "__main__":
    # execute only if run as a script
    main(sys.argv[1:])
    
    # # 测试
    # arg = ["--XCS_INTEGRATION_RESULT", "1",
    # "--XCS_SOURCE_DIR", "1",
    # "--XCS_PRODUCT", "1",
    # "--XCS_ERROR_COUNT", "1",
    # "--XCS_ERROR_CHANGE", "0",
    # "--XCS_WARNING_COUNT", "1",
    # "--XCS_WARNING_CHANGE", "-1",
    # "--XCS_ANALYZER_WARNING_COUNT", "1",
    # "--XCS_ANALYZER_WARNING_CHANGE", "1",
    # "--XCS_TEST_FAILURE_COUNT", "1",
    # "--XCS_TEST_FAILURE_CHANGE", "1",
    # "--XCS_TESTS_COUNT", "1",
    # "--XCS_TESTS_CHANGE", "1",
    # "--XCS_OUTPUT_DIR", "1",
    # "--XCS_PRIMARY_REPO_DIR", "1"
    # ]
    # main(arg)

