from lxml import html
from bs4 import BeautifulSoup
import re
import gc
import requests
from urllib import request
import urllib
import logging
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import ssl
from urllib3.util.ssl_ import create_urllib3_context
import socket
from requests.adapters import HTTPAdapter
import datetime
import pandas as pd
import time as ttime
import csv

driver = webdriver.Chrome(executable_path='./chromedrive/chromedriver.exe')
driver.set_page_load_timeout(30)

user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/63.0.3239.84 Chrome/63.0.3239.84 Safari/537.36'

# logging configuration
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

python_version = sys.version_info.major
logging.info("executed by python %d" % python_version)

ssl_context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)

CIPHERS = (
    'ECDH+AESGCM:DH+AESGCM:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:ECDH+HIGH:'
    'DH+HIGH:ECDH+3DES:DH+3DES:RSA+AESGCM:RSA+AES:RSA+HIGH:RSA+3DES:!aNULL:'
    '!eNULL:!MD5'
)
CIPHERS += (':DES-CBC3-SHA')

class SSLAdapter(HTTPAdapter):
    '''An HTTPS Transport Adapter that uses an arbitrary SSL version.'''

    def init_poolmanager(self, *args, **kwargs):
         context = create_urllib3_context(ciphers=CIPHERS)
         kwargs['ssl_context'] = context
         return super(SSLAdapter, self).init_poolmanager(*args, **kwargs)


if python_version == 3:
    import urllib.parse
    import urllib.request
    urljoin = urllib.parse.urljoin
    urlretrieve = urllib.request.urlretrieve
    quote = urllib.parse.quote

    # configure headers
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', user_agent)]
    urllib.request.install_opener(opener)


line = 2

def get_section_info(url):
    driver.get(url)
    ttime.sleep(1)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    body = soup.find(class_='race_table').find('tbody')
    res = {}
    sectional1 = ''
    sectional2 = ''
    sectional3 = ''
    sectional4 = ''
    sectional5 = ''
    sectional6 = ''
    for tr in body.find_all('tr'):
        td = tr.find_all('td')
        idx = td[0].get_text()
        sectional1_p = td[3].find_all('p')
        if sectional1_p:
            sectional1 = sectional1_p[-1].get_text()
        sectional2_p = td[4].find_all('p')
        if sectional2_p:
            sectional2 = sectional2_p[-1].get_text()
        sectional3_p = td[5].find_all('p')
        if sectional3_p:
            sectional3 = sectional3_p[-1].get_text()
        sectional4_p = td[6].find_all('p')
        if sectional4_p:
            sectional4 = sectional4_p[-1].get_text()
        sectional5_p = td[7].find_all('p')
        if sectional5_p:
            sectional5 = sectional5_p[-1].get_text()
        sectional6_p = td[8].find_all('p')
        if sectional6_p:
            sectional6 = sectional6_p[-1].get_text()
        one_res = []
        one_res.append(sectional1)
        one_res.append(sectional2)
        one_res.append(sectional3)
        one_res.append(sectional4)
        one_res.append(sectional5)
        one_res.append(sectional6)
        res[idx] = one_res
    return res

def get_comment_info(url):
    driver.get(url)
    ttime.sleep(1)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    body = soup.find('table', class_='table_bd').find('tbody')
    res = {}
    for tr in body.find_all('tr'):
        td = tr.find_all('td')
        idx = td[0].get_text()
        comment = td[5].get_text("|", strip=True)
        res[idx] = comment
    return res

def append_common_items(row, date, course, race, class_name, distance, prizemoney, going, time1, time2, time3, time4, time5, time6, race_sectional1, race_sectional2,\
    race_sectional3, race_sectional4, race_sectional5, race_sectional6):
    row.append(date)
    row.append(course)
    row.append(race)
    row.append(class_name)
    row.append(distance)
    row.append(prizemoney)
    row.append(going)
    row.append(time1)
    row.append(time2)
    row.append(time3)
    row.append(time4)
    row.append(time5)
    row.append(time6)
    row.append(race_sectional1)
    row.append(race_sectional2)
    row.append(race_sectional3)
    row.append(race_sectional4)
    row.append(race_sectional5)
    row.append(race_sectional6)
def append_special_items(row, plc, no, horse, jockey, trainer, ac_weight, horse_weight, draw, lbw, run, timestring, odds):
    row.append(plc)
    row.append(no)
    row.append(horse)
    row.append(jockey)
    row.append(trainer)
    row.append(ac_weight)
    row.append(horse_weight)
    row.append(draw)
    row.append(lbw)
    row.append(run)
    row.append(timestring)
    row.append(odds)

def append_section_info(rows, info):
    i = 0
    for idx in info:
        rows[i].append(info[idx][0])
        rows[i].append(info[idx][1])
        rows[i].append(info[idx][2])
        rows[i].append(info[idx][3])
        rows[i].append(info[idx][4])
        rows[i].append(info[idx][5])
        i+=1

def append_comment_info(rows, info):
    i = 0
    for idx in info:
        rows[i].append(info[idx])
        i += 1

fieldnames = ['DATE', 'COURSE', 'RACE', 'CLASS', 'DISTANCE', 'PRIZEMONEY', 'GOING', 'TIME1', 'TIME2', 'TIME3', 'TIME4', 'TIME5', 'TIME6'\
    , 'RACE_SECTIONAL1', 'RACE_SECTIONAL2', 'RACE_SECTIONAL3', 'RACE_SECTIONAL4', 'RACE_SECTIONAL5', 'RACE_SECTIONAL6', 'PLC', 'NO', 'HORSE', 'JOCKEY'\
        , 'TRAINER', 'AC Weight', 'Horse Weight', 'Draw', 'LBW', 'Run', 'Time', 'Odds', 'SECTIONAL1', 'SECTIONAL2', 'SECTIONAL3', 'SECTIONAL4'\
            , 'SECTIONAL5', 'SECTIONAL6', 'COMMENT']

def analyse_page1(url):

    global line

    driver.get(url)
    ttime.sleep(3)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    tt =soup.find('table', class_='js_racecard')
    buttons = soup.find('table', class_='js_racecard').find_all('td')
    button_id = 0
    button_len = len(buttons)
    button_url = driver.current_url
    while button_id < button_len-1:
        if button_id==0:
            button_id += 1
            continue
        cur_button_url = driver.current_url
        a_tag = buttons[button_id].find('a')
        if a_tag or button_url==cur_button_url:
            if a_tag:
                race_url = a_tag.get('href')
                race_url = urljoin(url, race_url)
                driver.get(race_url)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            ttime.sleep(1)
            datestring = soup.find('span', class_='f_fs13').get_text('|', strip=True).split(' ')[2].strip()
            race = soup.find(class_='race_tab').find("thead").find("tr").find("td").get_text('|', strip=True).split(' ')[1].strip()
            race_info = soup.find(class_='race_tab').find("tbody")
            horse_count = 0
            if race_info:
                trs = race_info.find_all("tr")
                tds = trs[1].find_all('td')
                class_distance = tds[0].get_text()
                segments = class_distance.split('-')
                class_name = segments[0].strip()
                distance = segments[1].strip()
                going = tds[2].get_text()
                tds = trs[2].find_all('td')
                course = tds[2].get_text()
                tds = trs[3].find_all('td')
                i = 0
                prize_money = ''
                time1 = ''
                time2 = ''
                time3 = ''
                time4 = ''
                time5 = ''
                time6 = ''
                rows = []
                for td in tds:
                    if i == 0:
                        prize_money = td.get_text()
                        prize_money = prize_money.split(' ')[1].strip()
                    elif i==2:
                        time1 = td.get_text()
                        if time1[0]=='(':
                            time1 = time1[1:-1]
                    elif i==3:
                        time2 = td.get_text()
                        if time2[0]=='(':
                            time2 = time2[1:-1]
                    elif i==4:
                        time3 = td.get_text()
                        if time3[0]=='(':
                            time3 = time3[1:-1]
                    elif i==5:
                        time4 = td.get_text()
                        if time4[0]=='(':
                            time4 = time4[1:-1]
                    elif i==6:
                        time5 = td.get_text()
                        if time5[0]=='(':
                            time5 = time5[1:-1]
                    elif i==7:
                        time6 = td.get_text()
                        if time6[0]=='(':
                            time6 = time6[1:-1]
                    i += 1
                race_sectional1 = 0
                race_sectional2 = 0
                race_sectional3 = 0
                race_sectional4 = 0
                race_sectional5 = 0
                race_sectional6 = 0
                i = 0
                tds = trs[4].find_all('td')
                for td in tds:
                    if i == 2:
                        race_sectional1 = td.get_text()
                    elif i == 3:
                        race_sectional2 = td.get_text()
                    elif i == 4:
                        race_sectional3 = td.get_text()
                    elif i == 5:
                        race_sectional4 = td.get_text()
                    elif i == 6:
                        race_sectional5 = td.get_text()
                    elif i == 7:
                        race_sectional6 = td.get_text()
                    i += 1
                table_performance = soup.find(class_='performance').find('tbody')
                if table_performance:
                    all_records = table_performance.find_all('tr')
                    horse_count = len(all_records)
                    for tr in all_records:
                        row = []
                        append_common_items(row, datestring, course, race, class_name, distance, prize_money, going, time1, time2, time3, time4, time5, time6,
                            race_sectional1, race_sectional2, race_sectional3, race_sectional4, race_sectional5, race_sectional6)
                        i = 0
                        for td in tr.find_all('td'):
                            if i==0:
                                plc = td.get_text("|", strip=True)
                            elif i==1:
                                no = td.get_text("|", strip=True)
                            elif i==2:
                                horse = td.get_text("|", strip=True)
                            elif i==3:
                                jockey = td.get_text("|", strip=True)
                            elif i==4:
                                trainer = td.get_text("|", strip=True)
                            elif i==5:
                                ac_weight = td.get_text("|", strip=True)
                            elif i==6:
                                horse_weight = td.get_text("|", strip=True)
                            elif i==7:
                                draw = td.get_text("|", strip=True)
                            elif i==8:
                                lbw = td.get_text("|", strip=True)
                            elif i==9:
                                run = ''
                                div = td.find('div')
                                if div:
                                    div = div.find_all('div')
                                    for d in div:
                                        r = d.get_text("|", strip=True)
                                        if d == div[0]:
                                            run += r
                                        else:
                                            run += ('-' + r)
                            elif i==10:
                                timestring = td.get_text("|", strip=True)
                            elif i==11:
                                odds = td.get_text("|", strip=True)
                            i+=1
                        append_special_items(row, plc, no, horse, jockey, trainer, ac_weight, horse_weight, draw, lbw, run, timestring, odds)
                        
                        line += 1
                        rows.append(row)

                    section_url = soup.find(class_='sectional_time_btn').find('a').get('href')
                    section_url = urljoin(url, section_url)
                    ttime.sleep(1)
                    section_info = get_section_info(section_url)
                    append_section_info(rows, section_info)
                    comment_item = soup.find(id='racerunningpositionphotos')
                    ttime.sleep(1)
                    if comment_item:
                        comment_item = comment_item.find('p', class_='f_tar')
                        if comment_item:
                            comment_item = comment_item.find('a')
                            if comment_item:
                                comment_url = comment_item.get('href')
                                comment_url = urljoin(url, comment_url)
                                comment_info = get_comment_info(comment_url)
                                append_comment_info(rows, comment_info)
                writer.writerows(rows)
        driver.get(button_url)
        ttime.sleep(1)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        buttons = soup.find('table', class_='js_racecard').find_all('td')
        button_id += 1




if __name__ == "__main__":
    fp = open("url.txt", "r")
    with open('Scraping1.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)
        for url in fp:
            analyse_page1(url)

    fp.close()