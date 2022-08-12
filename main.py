#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import requests
from bs4 import BeautifulSoup

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'ja;q=0.5',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://www.houjin-bangou.nta.go.jp',
    'Referer': 'https://www.houjin-bangou.nta.go.jp/kensaku-kekka.html',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Sec-GPC': '1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36',
}

company_name = input("CompanyName: ")

data = 'jp.go.nta.houjin_bangou.framework.web.common.CNSFWTokenProcessor.request.token=8e950daf-8269-40de-9d55-e01693e887a6&viewNumAnc=10&kjscr0201010m1Table.specifiedPageNumber=1&houzinNmShTypeRbtn=2&houzinNmTxtf='+company_name+'&_kanaCkbx=on&_noconvCkbx=on&houzinAddrShTypeRbtn=1&prefectureLst=&houzinNoShTyoumeSts=0&kokugaiTxtf=&zipCdTxtf=&houzinNoShSonotaZyoukenSts=&_houzinKdCkbx=on&_houzinKdCkbx=on&_houzinKdCkbx=on&_houzinKdCkbx=on&_houzinKdCkbx=on&_houzinKdCkbx=on&_houzinKdCkbx=on&_houzinKdCkbx=on&_historyCkbx=on&_hideCkbx=on&_closeCkbx=on&_chgYmdShTargetCkbx=on&chgYmdEyFromLst=000&chgYmdMFromLst=00&chgYmdDFromLst=00&chgYmdEyToLst=000&chgYmdMToLst=00&chgYmdDToLst=00&orderRbtn=1&viewPageNo=1&preSyousaiScreenId=KJSCR0201010&searchFlg=1'

data = data.encode('utf-8')

response = requests.post('https://www.houjin-bangou.nta.go.jp/kensaku-kekka.html', headers=headers, data=data)

soup = BeautifulSoup(response.content, "html.parser")

first_company = soup.select("#contents > main > div.box01.print01 > div > div.tbl01 > table > tbody > tr > th")[0].text

first_company_num = re.sub(r"\D", "", first_company)

print("法人番号: "+first_company_num)

# ここから従業員数調べ

cookies = {
    'JSESSIONID': 'E9A5229582B3C38229E829DC83424782',
    'visid_incap_2386852': 'y9rFQYhMShWI/R2J3jtHvlR57mIAAAAAQUIPAAAAAABwSXv1yWlRZOheZQ6xPO1y',
    'Setting': '1%3A0',
    'incap_ses_636_2386852': '+cCnTyUa+R0cgBgESYfTCGd182IAAAAAO24tvPiVS43Ul1snA7mOnw==',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'ja;q=0.5',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    # Requests sorts cookies= alphabetically
    # 'Cookie': 'JSESSIONID=E9A5229582B3C38229E829DC83424782; visid_incap_2386852=y9rFQYhMShWI/R2J3jtHvlR57mIAAAAAQUIPAAAAAABwSXv1yWlRZOheZQ6xPO1y; Setting=1%3A0; incap_ses_636_2386852=+cCnTyUa+R0cgBgESYfTCGd182IAAAAAO24tvPiVS43Ul1snA7mOnw==',
    'Origin': 'https://www2.nenkin.go.jp',
    'Referer': 'https://www2.nenkin.go.jp/do/search_section',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Sec-GPC': '1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36',
}

data = {
    'hdnPrefectureCode': '',
    'hdnSearchOffice': '1',
    'hdnSearchCriteria': '3',
    'txtOfficeName': '',
    'txtOfficeAddress': '',
    'txtHoujinNo': str(first_company_num),
    'hdnDisplayItemsRestorationScreenDto': '',
    'hdnDisplayItemsRestorationScreenDtoKeepParam': 'false',
    'gmnId': 'GB10001SC010',
    'hdnErrorFlg': '',
    'eventId': '/SEARCH.HTML',
    '/search.html': '',
}

response = requests.post('https://www2.nenkin.go.jp/do/search_section', cookies=cookies, headers=headers, data=data)

soup = BeautifulSoup(response.content, "html.parser")

member_count = soup.select("#CONT > div.return_Boxcont > table > tr:nth-child(2) > td.search_right_top")

print(member_count)

print("正社員: "+member_count[0].text)
