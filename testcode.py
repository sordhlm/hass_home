#!/usr/bin/env python
#coding=utf-8
'''
'''

import os
import time,datetime
import re
import requests
import json

class AirvisualAPI(object):

    def __init__(self, city="Hangzhou", state="Zhejiang", \
            country="China", key="embEDMGfLvPua7d7A"):
        url = "http://api.airvisual.com/v2/city"
        querystring = {"city":"%s"%city,"state":"%s"%state,"country":"%s"%country,"key":"%s"%key}
        self.data = json.loads(requests.get(url, params=querystring).text)

    def __getitem__(self,key):
        return self.data['data']['current']['pollution'][key]

if __name__ == '__main__':

    air = AirvisualAPI()
    print air['aqicn']
    #url = "http://api.airvisual.com/v2/city"
    #
    #querystring = {"city":"Hangzhou","state":"Zhejiang","country":"China","key":"embEDMGfLvPua7d7A"}
    #
    ##response = requests.request("GET", url, params=querystring)
    #response = requests.get(url, params=querystring)
    #print(response.text)
    #data = json.loads(response.text)
    #print(data['data']['current']['pollution'])
