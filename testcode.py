#!/usr/bin/env python
#coding=utf-8
'''
'''

import os
import time,datetime
import re
import requests

if __name__ == '__main__':


    url = "http://api.airvisual.com/v2/city"

    querystring = {"city":"Hangzhou","state":"Zhejiang","country":"China","key":"embEDMGfLvPua7d7A"}

    response = requests.request("GET", url, params=querystring)
    print("sssssssssss")
    print(response.text)

