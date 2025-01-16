########################################################
#        Program to Download Wallpapers from           #
#                  alpha.wallhaven.cc                  #
#                                                      #
#                 Author - Saurabh Bhan                #
#                                                      #
#                  Dated- 26 June 2016                 #
#                 Update - 11 June 2019                #
########################################################

import os
import getpass
import re
import requests
import tqdm
import time
import urllib
import json

folderName = 'toplist240'

# 创建名为 'Wallhaven' 的目录，如果已存在则不报错
os.makedirs(folderName, exist_ok=True)
BASEURL=""
cookies=dict()

global APIKEY
APIKEY = "ryYyavZRvlFq0r2eHo88fGu9CDhEZCIn"

def category():
    global BASEURL
    print('''
    ****************************************************************
                            Category Codes

    all     - Every wallpaper.
    general - For 'general' wallpapers only.
    anime   - For 'Anime' Wallpapers only.
    people  - For 'people' wallapapers only.
    ga      - For 'General' and 'Anime' wallapapers only.
    gp      - For 'General' and 'People' wallpapers only.
    ****************************************************************
    ''')
    # 输入类别代码
    ccode = input('Enter Category: ').lower()
    ctags = {'all':'111', 'anime':'010', 'general':'100', 'people':'001', 'ga':'110', 'gp':'101' }
    ctag = ctags[ccode]

    print('''
    ****************************************************************
                            Purity Codes

    sfw     - For 'Safe For Work'
    sketchy - For 'Sketchy'
    nsfw    - For 'Not Safe For Work'
    ws      - For 'SFW' and 'Sketchy'
    wn      - For 'SFW' and 'NSFW'
    sn      - For 'Sketchy' and 'NSFW'
    all     - For 'SFW', 'Sketchy' and 'NSFW'
    ****************************************************************
    ''')
    # 输入纯度代码
    pcode = input('Enter Purity: ')
    ptags = {'sfw':'100', 'sketchy':'010', 'nsfw':'001', 'ws':'110', 'wn':'101', 'sn':'011', 'all':'111'}
    ptag = ptags[pcode]

    # 构建 API 请求的基础 URL
    BASEURL = 'https://wallhaven.cc/api/v1/search?apikey=' + APIKEY + "&categories=" +\
        ctag + '&purity=' + ptag + '&page='

def latest():
    global BASEURL
    print('Downloading latest')
    topListRange = '1M'
    # 构建下载最新壁纸的 API 请求 URL
    BASEURL = 'https://wallhaven.cc/api/v1/search?apikey=' + APIKEY + '&topRange=' +\
    topListRange + '&sorting=toplist&page='

def search():
    global BASEURL
    query = input('Enter search query: ')
    # 构建搜索壁纸的 API 请求 URL
    BASEURL = 'https://wallhaven.cc/api/v1/search?apikey=' + APIKEY + '&q=' + \
        urllib.parse.quote_plus(query) + '&page='

def toplist():
    global BASEURL
    print('Downloading toplist')
    # 构建下载排行榜壁纸的 API 请求 URL
    BASEURL = 'https://wallhaven.cc/api/v1/search?apikey=' + APIKEY + '&categories=111&purity=100&topRange=3M&sorting=toplist&order=desc&ai_art_filter=1&page='

def downloadPage(pageId, totalImage):
    url = BASEURL + str(pageId)
    urlreq = requests.get(url, cookies=cookies)
    pagesImages = json.loads(urlreq.content)
    pageData = pagesImages["data"]

    for i in range(len(pageData)):
        currentImage = (((pageId - 1) * 24) + (i + 1))

        url = pageData[i]["path"]
        
        filename = os.path.basename(url)
        osPath = os.path.join(folderName, filename)
        if not os.path.exists(osPath):
            imgreq = requests.get(url, cookies=cookies)
            if imgreq.status_code == 200:
                print("Downloading : %s - %s / %s" % (filename, currentImage , totalImage))
                with open(osPath, 'ab') as imageFile:
                    for chunk in imgreq.iter_content(1024):
                        imageFile.write(chunk)
            elif (imgreq.status_code != 403 and imgreq.status_code != 404):
                print("Unable to download %s - %s / %s" % (filename, currentImage , totalImage))
        else:
            print("%s already exist - %s / %s" % (filename, currentImage , totalImage))

def main():
    Choice = input('''Choose how you want to download the image:

    Enter "category" for downloading wallpapers from specified categories
    Enter "latest" for downloading latest wallpapers
    Enter "toplist" for downloading top list wallpapers
    Enter "search" for downloading wallpapers from search

    Enter choice: ''').lower()
    while Choice not in ['category', 'latest', 'search', 'toplist']:
        if Choice != None:
            print('You entered an incorrect value.')
        choice = input('Enter choice: ')

    if Choice == 'category':
        category()
    elif Choice == 'latest':
        latest()
    elif Choice == 'toplist':
        toplist()
    elif Choice == 'search':
        search()

    pgid = int(input('How Many pages you want to Download: '))
    totalImageToDownload = str(24 * pgid)
    print('Number of Wallpapers to Download: ' + totalImageToDownload)
    for page_index in range(1, pgid + 1):
        downloadPage(page_index, totalImageToDownload)

if __name__ == '__main__':
    main()
