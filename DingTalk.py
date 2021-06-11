
#!/usr/bin/env python3
import requests
from requests_toolbelt import MultipartEncoder
import time
import hmac
import hashlib
import base64
import urllib.parse
import sys, getopt


# 打包群
ding_Talk_rboot = ''
ding_Talk_secret=''

# ************************************************

# 钉钉文档
# https://ding-doc.dingtalk.com/doc#/serverapi2/qf2nxq

def getSign():
    timestamp = str(round(time.time() * 1000))
    secret = ding_Talk_secret
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    return (timestamp, sign)

def getDingTalkRbootUrl():
    sign = getSign()
    return "{0}&timestamp={1}&sign={2}".format(ding_Talk_rboot, sign[0], sign[1])
