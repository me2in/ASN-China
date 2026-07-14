'''
Author: Vincent Young
Date: 2022-11-17 02:14:24
LastEditors: Vincent Young
LastEditTime: 2022-11-17 03:19:20
FilePath: /ASN-China/syncIP.py
Telegram: https://t.me/missuo

Copyright © 2022 by Vincent, All Rights Reserved. 
'''

import os

import requests

allChina = "https://raw.githubusercontent.com/cbuijs/ipasn/master/country-asia-china.list"

v4China = "https://raw.githubusercontent.com/cbuijs/ipasn/master/country-asia-china4.list"

v6China = "https://raw.githubusercontent.com/cbuijs/ipasn/master/country-asia-china6.list"

def syncFile(url, fileName):
    content = requests.get(url).content
    if os.path.exists(fileName):
        with open(fileName, "rb") as f:
            if f.read() == content:
                print("{}: no changes, skip updating.".format(fileName))
                return
    with open(fileName, "wb") as f:
        f.write(content)
    print("{}: updated.".format(fileName))

syncFile(allChina, "IP.China.list")
syncFile(v4China, "IPv4.China.list")
syncFile(v6China, "IPv6.China.list")
