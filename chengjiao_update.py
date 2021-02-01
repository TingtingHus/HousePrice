#!/usr/bin/python4
# -*- coding: utf-8 -*-
# @Time    : 2020/11/10 4:07 下午
# @Author  : Huting
from __future__ import unicode_literals
import logging
import random
import re
import time
import traceback
import datetime
import requests
from bs4 import BeautifulSoup
from requests import RequestException
import json
import sys

ds = ['/chengjiao/pidou/','/chengjiao/longquanyi/','/chengjiao/xindou/','/chengjiao/qingbaijiang/','/chengjiao/doujiangyan/','/chengjiao/pengzhou/','/chengjiao/jianyang/','/chengjiao/xinjin/','/chengjiao/chongzhou1/','/chengjiao/dayi/','/chengjiao/jintang/', '/chengjiao/pujiang/','/chengjiao/qionglai/']


def get_page(url, user_agent):
    try:
        response = requests.get(url, headers={
            "User-Agent": user_agent,
            "Cookie": "ab_jid_BFESS=cec15f32ad500d3c413fee65851958ac1596; BDUSS_BFESS=1R2bkZwVnhSYVBTYkxoNmw5Vjd1MHNBQUFSZ0VLM2tEaGdSelhJflZmU1lIcGRlRVFBQUFBJCQAAAAAAAAAAAEAAAB7LgAMzMbDxbvGwM~QsAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJiRb16YkW9eZ; BAIDUID_BFESS=B0DEF93359EDD0232205059B9DC9416B:FG=1",
            "Origin": "https://cd.lianjia.com",
            "Referer": "https://cd.lianjia.com/"
        })
        if response.status_code == 200:
            return response.text
        return "response.text != 200"
    except RequestException:
        return None


def get_distinct(url, distinct_list, user_agent):
    html_distinct = get_page(url,user_agent)
    soup = BeautifulSoup(html_distinct, 'html.parser')
    soup = soup.find('div', attrs={'data-role': 'ershoufang'})
    links = soup.find_all('a')
    for one in links:
        distinct_list.append(one.get('href'))
    return distinct_list


def get_num(url, user_agent):
    html_num = get_page(url,user_agent)
    soup_num = BeautifulSoup(html_num, 'html.parser')
    sub_num = soup_num.find('div', attrs={'class': 'page-box house-lst-page-box'})
    if sub_num is not None:
        house_page = int(sub_num.get('page-data').split(',')[0].split(':')[1])
    else:
        house_page = 0
    return house_page


def get_house_id(page):
    soup = BeautifulSoup(page, 'html.parser').find_all('ul',attrs={'class':'listContent'})
    ids = soup[0].find_all('li')
    house_ids = []
    for one_id in ids:
        id_link = one_id.find('div',attrs={'class':'title'}).find('a').get('href')
        pattern_class = re.compile(r'[0-9]+')
        house_id = pattern_class.findall(id_link)
        house_ids.append(house_id)
    return house_ids


def house_info(id_num, user_agent):
    url = 'https://cd.lianjia.com/chengjiao/' + id_num[0] + '.html'
    html = get_page(url,user_agent)
    soup = BeautifulSoup(html, 'html.parser')
    house_dict = dict.fromkeys(
            {'id','domain', 'tenant_id', 'name', 'type', 'deal_dt', 'location', 'sub_location', 'area', 'class', 'avg_price',
             'total_price','used_price','period','change_time','introduce','follower','views','build_time','zhuangxiu',
             'show_time','years','other'})
    pattern_class = re.compile(r'[0-9]室')
    pattern_area = re.compile(r'[0-9+.?[0-9]+㎡')

    house_dict['id'] = id_num[0]
    house_dict['domain'] = '已成交二手房'
    house_dict['tenant_id'] = soup.find('div',attrs={'class':'deal-bread'}).get_text().split('>')[2].split('二手房')[0]
    house_dict['name'] = soup.find('div', attrs={'class': 'deal-bread'}).get_text().split('>')[4].split('二手房')[0]
    house_dict['type'] = soup.find('div', attrs={'class': 'introContent'}).find_all('li')[16].get_text().strip().split('房屋用途')[1]
    house_dict['deal_dt'] = soup.find('div', attrs={'class': 'wrapper'}).find('span').get_text().split(' ')[0]
    house_dict['location'] = soup.find('div', attrs={'class': 'deal-bread'}).get_text().split('>')[2].split('二手房')[0]
    house_dict['sub_location'] = soup.find('div',attrs={'class':'deal-bread'}).get_text().split('>')[3].split('二手房')[0]
    house_dict['area'] = pattern_area.findall(soup.find('div', attrs={'class': 'introContent'}).find_all('li')[2].get_text().strip())
    house_dict['class'] = pattern_class.findall(soup.find('div', attrs={'class': 'introContent'}).find_all('li')[0].get_text().strip())
    house_dict['avg_price'] = soup.find('div', attrs={'class': 'info fr'}).find('b').get_text()
    house_dict['total_price'] = soup.find('div', attrs={'class': 'info fr'}).find('span',class_='dealTotalPrice').get_text()
    house_dict['used_price'] = soup.find('div', attrs={'class': 'msg'}).find_all('span')[0].get_text()
    house_dict['period'] = soup.find('div', attrs={'class': 'msg'}).find_all('span')[1].get_text()
    house_dict['change_time'] = soup.find('div', attrs={'class': 'msg'}).find_all('span')[2].get_text()
    house_dict['introduce'] = soup.find('div', attrs={'class': 'msg'}).find_all('span')[3].get_text()
    house_dict['follower'] = soup.find('div', attrs={'class': 'msg'}).find_all('span')[4].get_text()
    house_dict['views'] = soup.find('div', attrs={'class': 'msg'}).find_all('span')[5].get_text()
    house_dict['build_time'] = soup.find('div', attrs={'class': 'introContent'}).find_all('li')[7].get_text().strip()
    house_dict['zhuangxiu'] = soup.find('div', attrs={'class': 'introContent'}).find_all('li')[8].get_text().strip()
    house_dict['show_time'] = soup.find('div', attrs={'class': 'introContent'}).find_all('li')[15].get_text().strip()
    house_dict['years'] = soup.find('div', attrs={'class': 'introContent'}).find_all('li')[17].get_text().strip().split('房屋年限')[1]
    house_dict['other'] = soup.find('div', attrs={'class': 'introContent'}).find_all('li')[18].get_text().strip()
    return house_dict


def chengjiao_data():
    home = 'https://cd.lianjia.com/chengjiao/'
    user_agents = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
        'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)']
    distincts = []
    logging.info("begin get distinct")
    try:
        distincts = get_distinct(home, distincts, user_agents[random.randint(0, 10)])
        logging.info("success to get distinct data")
        print("success to get distinct data")
        with open('chengjiao0125', 'a+') as f:
            for distinct in distincts:
                if distinct in ds:
                    print("{distinct} no need get".format(distinct=distinct))
                    continue
                distinct_page = 'https://cd.lianjia.com' + distinct
                logging.info('The {distinct} data is begining'.format(distinct=distinct))
                try:
                    nums = get_num(distinct_page, user_agents[random.randint(0, 10)])
                    logging.info("success to get {distinct}'s page {nums} and begin get page's house ids".format(distinct=distinct,nums=nums))
                    print("success to get {distinct}'s page {nums} and begin get page's house ids".format(distinct=distinct,nums=nums))
                    num = 1
                    while num <= nums:
                        page_url = 'https://cd.lianjia.com' + distinct + 'pg' + str(num)
                        try:
                            html = get_page(page_url, user_agents[random.randint(0, 10)])
                            houses = get_house_id(html)
                            logging.info("success to get {distinct} {num}'s ids and begin each house_info".format(distinct=distinct,num=num))
                            print("success to get {distinct} {num}'s ids and begin each house_info".format(distinct=distinct,num=num))
                            for house in houses:
                                try:
                                    myhouse = house_info(house, user_agents[random.randint(0, 10)])
                                    d = json.dumps(myhouse).encode("utf-8").decode("utf-8")
                                    # print(d)
                                    f.write(d + "\n")
                                    f.flush()
                                    logging.info("success to get {house} info and sleep and next id".format(house=house))
                                    print("success to get {house} info and sleep and next id".format(house=house))
                                    time.sleep(5 + random.randint(0, 10))
                                except:
                                    exceptionInfo()
                                    logging.info("fail to get {house} however sleep and next id".format(house=house))
                                    print("fail to get {house} however sleep and next id".format(house=house))
                                    time.sleep(30 + random.randint(0, 60))
                            num = num + 1
                        except:
                            exceptionInfo()
                            logging.info(
                                "fail to get {distinct} {num}'s ids then next page".format(distinct=distinct, num=num))
                            print("fail to get {distinct} {num}'s ids then next page".format(distinct=distinct, num=num))
                            num = num + 1
                except:
                    exceptionInfo()
                    logging.info('fail to get {distinct} page number so next distinct'.format(distinct=distinct))
                    print('fail to get {distinct} page number so next distinct'.format(distinct=distinct))
    except:
        exceptionInfo()
        logging.info('fail to get distinct')
        logging.info("process failed when getting distinct")


def exceptionInfo():
    ex_type, ex_val, ex_stack = sys.exc_info()
    logging.info(ex_type)
    logging.info(ex_val)
    for stack in traceback.extract_tb(ex_stack):
        logging.info(stack)


if __name__ == "__main__":
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(filename='chengjiao0125.log', level=logging.INFO, format=LOG_FORMAT)

    logging.info("Begin process")
    chengjiao_data()
