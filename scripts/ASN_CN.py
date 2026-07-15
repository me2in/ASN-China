'''
Author: Vincent Young
Date: 2022-11-17 02:29:30
LastEditors: Vincent Young
LastEditTime: 2022-11-17 03:46:25
FilePath: /ASN-China/scripts/ChinaASN.py
Telegram: https://t.me/missuo

Copyright © 2022 by Vincent, All Rights Reserved. 
'''
import os
import time

import requests
from lxml import etree

FILE_NAME = "ASN.China.list"

def fetchLatestASN():
    url = "https://bgp.he.net/country/CN"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }
    r = requests.get(url = url, headers = headers).text
    tree = etree.HTML(r)
    asns = tree.xpath('//*[@id="asns"]/tbody/tr')
    entries = []
    for asn in asns:
        asnNumber = asn.xpath('td[1]/a')[0].text.replace('AS', '')
        asnName = asn.xpath('td[2]')[0].text
        if asnName != None:
            entries.append((asnNumber, asnName.strip()))
    return entries

def readExistingEntries():
    if not os.path.exists(FILE_NAME):
        return None
    entries = []
    prevLine = ""
    with open(FILE_NAME, "r") as asnFile:
        for line in asnFile:
            line = line.rstrip("\n")
            if line.startswith("IP-ASN,"):
                name = prevLine[3:] if prevLine.startswith("// ") else ""
                entries.append((line[len("IP-ASN,"):], name))
            prevLine = line
    return entries

def writeFile(entries):
    localTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    with open(FILE_NAME, "w") as asnFile:
        asnFile.write("// ASN Information in China. (https://github.com/missuo/ASN-China)\n")
        asnFile.write("// Last Updated: UTC " + localTime + "\n")
        asnFile.write("// Made by Vincent, All rights reserved.\n\n")
        for asnNumber, asnName in entries:
            asnFile.write("// {}\nIP-ASN,{}\n".format(asnName, asnNumber))

def sortedEntries(entries):
    return sorted(entries)

def saveLatestASN():
    entries = fetchLatestASN()
    if not entries:
        print("No ASN data fetched, keep existing file.")
        return
    existing = readExistingEntries()
    if existing is not None:
        if existing == entries:
            print("{}: no changes, skip updating.".format(FILE_NAME))
            return
        if sortedEntries(existing) == sortedEntries(entries):
            print("{}: only order changed, skip updating.".format(FILE_NAME))
            return
    writeFile(entries)
    print("{}: ASN entries changed, file updated.".format(FILE_NAME))

saveLatestASN()
