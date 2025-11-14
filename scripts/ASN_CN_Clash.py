'''
Author: Vincent Young
Date: 2022-11-17 02:29:30
LastEditors: Vincent Young
LastEditTime: 2022-11-17 03:46:25
FilePath: /ASN-China/scripts/ASN_CN_CLASH.py
Telegram: https://t.me/missuo

Copyright © 2022 by Vincent, All Rights Reserved. 
'''
import requests
from lxml import etree
import time

def initFile():
    localTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    with open("ASN.China.Clash.txt", "w", encoding="utf-8") as clashFile:
        clashFile.write("# ASN Information in China. (https://github.com/missuo/ASN-China) \n")
        clashFile.write("# Last Updated: UTC " + localTime + "\n")
        clashFile.write("# Made by Vincent, All rights reserved. " + "\n\n")

def saveLatestASN():
    url = "https://bgp.he.net/country/CN"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }
    r = requests.get(url = url, headers = headers).text
    tree = etree.HTML(r)
    asns = tree.xpath('//*[@id="asns"]/tbody/tr')
    initFile()
    for asn in asns:
        asnNumber = asn.xpath('td[1]/a')[0].text.replace('AS','')
        asnName = asn.xpath('td[2]')[0].text
        if asnName != None:
            clashInfo = "IP-ASN,{} # {}".format(asnNumber, asnName)
            with open("asn.china.txt", "a", encoding="utf-8") as clashFile:
                clashFile.write(clashInfo)
                clashFile.write("\n")

saveLatestASN()

