from bs4 import BeautifulSoup
# import re
# from lxml import html
# import gc
# import requests
# from urllib import request
# import urllib
# import logging
# import time
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import time as ttime
import xlsxwriter
import xlrd
from operator import itemgetter, attrgetter

driver = webdriver.Chrome(executable_path='./chromedrive/chromedriver.exe')
driver.set_page_load_timeout(50)

user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/63.0.3239.84 Chrome/63.0.3239.84 Safari/537.36'

python_version = sys.version_info.major

DAYS = ('Ma', 'Ti', 'Ke', 'To', 'Pe', 'La', 'Su')



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


line = 3
workbook = xlsxwriter.Workbook('Liiga.xlsx')
worksheet = workbook.add_worksheet()

def find_specific_item_with_text(root, tagname, classname, text):
    items = root.find_all(tagname, class_=classname)
    if items == None:
        return None
    for item in items:
        text_item = item.get_text('|', strip=True)
        if text_item.find(text) != -1:
            return item
    return None

def analyse_page1(url):

    global line

    try:
        driver.get(url)
        ttime.sleep(2)
    except:
        driver.get(url)
        ttime.sleep(2)
#        driver.delete_all_cookies()
        return

    soup = BeautifulSoup(driver.page_source, "html.parser")
#    trs = driver.find_elements_by_xpath('//table[@class="games-list-table"]/tbody/tr') #
    trs = soup.find('table', class_='games-list-table').find('tbody').find_all('tr')
    for tr in trs:
        tds = tr.find_all('td')
        date_day = tds[1].get_text('|', strip=True)
        day = ''
        date = ''
        if date_day.find(' ') != -1:
            day = date_day.split(' ')[0].strip()
            date = date_day.split(' ')[1].strip()
        home_away = tds[3].get_text('|', strip=True)
        home = home_away.split('-')[0].strip()
        away = home_away.split('-')[1].strip() 
        if tds[4].find('a', title='Seuranta') == None:
            continue
        link_url = tds[4].find('a', title='Seuranta').get('href')
        link_url = urljoin(url, link_url)
        try:
            driver.get(link_url)
            ttime.sleep(1)
        except:
            driver.get(link_url)
            ttime.sleep(1)
        soup1 = BeautifulSoup(driver.page_source, "html.parser")
        tbody = soup1.find('table').find('tbody')
        goal_keeper = find_specific_item_with_text(tbody, 'tr', 'period', 'Maalivahdit').find_next_sibling('tr') #soup1.find(class_='period').find(text='Maalivahdit').parent.find_next_sibling()
        item = goal_keeper.find_all('td')
        keeper_item1 = item[0].find('a')
        home_keeper = keeper_item1.get_text('|', strip=True)
        store_item1 = keeper_item1.next_sibling
        home_store = store_item1.strip() #store_item1.get_text('|', strip=True)
        home_store = home_store.split('=')[-1].strip()
        keeper_item2 = item[2].find('a')
        away_keeper = keeper_item2.get_text('|', strip=True)
        store_item2 = keeper_item2.next_sibling
        away_store = store_item2.strip() #.get_text('|', strip=True)        
        away_store = away_store.split('=')[-1].strip()
        TM = find_specific_item_with_text(tbody, 'tr', 'period', '3. erä').find_next_sibling('tr')
        TM_home = 0
        TM_home_str = ''
        TM_away = 0
        TM_away_str = ''
        while TM.get_text('|', strip=True) != 'Maalivahdit':
            if TM.find('strong') and TM.find('strong').get_text().find('TM') != -1:
                strong_elem_home = TM.find('td', class_='home').find('strong')
                if strong_elem_home:
                    TM_user_homes = strong_elem_home.find_next_siblings('a')
                    if TM_user_homes:
                        for TM_user_home in TM_user_homes:
                            TM_val_home = TM_user_home.next_sibling.strip("(), \n")
                            TM_val_home = TM_val_home.strip()
                            TM_home += int(TM_val_home)
                            if TM_user_home != TM_user_homes[0]:
                                TM_home_str += ','
                            TM_home_str += TM_val_home
                strong_elem_away = TM.find('td', class_='away').find('strong')
                if strong_elem_away:
                    TM_user_aways = strong_elem_away.find_next_sibling('a')
                    if TM_user_aways:
                        for TM_user_away in TM_user_aways:
                            TM_val_away = TM_user_away.next_sibling.strip("(), \n")
                            TM_val_away = TM_val_away.strip()
                            TM_away += int(TM_val_away)
                            if TM_user_away != TM_user_aways[0]:
                                TM_away_str += ','
                            TM_away_str += TM_val_away

            TM = TM.find_next_sibling('tr')

        worksheet.write('A'+str(line), day)
        worksheet.write('B'+str(line), date)
        worksheet.write('C'+str(line), home)
        worksheet.write('D'+str(line), away)
        worksheet.write('E'+str(line), home_keeper)
        worksheet.write('F'+str(line), away_keeper)
        worksheet.write('G'+str(line), home_store)
        worksheet.write('H'+str(line), away_store)
        worksheet.write('I'+str(line), TM_home_str)
        worksheet.write('J'+str(line), TM_away_str)
#        worksheet.write('I'+str(line), str(TM_home))
#        worksheet.write('J'+str(line), str(TM_away))
        worksheet.write('K'+str(line), link_url)
        driver.back()
        ttime.sleep(1)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        trs = soup.find('table', class_='games-list-table').find('tbody').find_all('tr')
#        trs = driver.find_elements_by_xpath('//table[@class="games-list-table"]/tbody/tr')
        line += 1

    workbook.close()

def get_pure_store_value(in_str):
    items = in_str.split('=')
    total = int(items[-1].strip())
    expression_str = items[0].strip()
    additionals = expression_str.split('+')
    if len(additionals)==4:
        total = total - int(additionals[3])
    return total

def analyse_page2(url, res, season, date_all_flg, date_from, date_to):

    # driver.get(url)
    # ttime.sleep(1)
    option_season = driver.find_element_by_xpath("//select[@name='season']").find_elements_by_tag_name("option")
    for option in option_season:
        if option.text == season:
            option.click()
            ttime.sleep(1)
            break
    curr_url = driver.current_url
    # try:
    #     driver.get(curr_url)
    #     ttime.sleep(2)
    # except:
    #     driver.get(curr_url)
    #     ttime.sleep(2)
    #     return

    ii = 0
    driver1 = webdriver.Chrome(executable_path='./chromedrive/chromedriver.exe')
    driver1.set_page_load_timeout(50)

    soup = BeautifulSoup(driver.page_source, "html.parser")
#    trs = driver.find_elements_by_xpath('//table[@class="games-list-table"]/tbody/tr') #
    trs = soup.find('table', class_='games-list-table').find('tbody').find_all('tr')
    prev_date = ''
    for tr in trs:
        ii += 1
        # if ii == 110:
        #     driver1.close()
        #     return 0
        tds = tr.find_all('td')
        date_day = tds[1].get_text('|', strip=True)
        day = ''
        date = ''
        if date_day.find(' ') != -1:
            day = date_day.split(' ')[0].strip()
            date = date_day.split(' ')[1].strip()
            d, m, y = [int(x) for x in date.split('.')]
            prev_date = datetime.date(y, m, d)
            prev_date_string = date
            prev_day = day
        if date_all_flg != True:
            if date_from > prev_date or date_to < prev_date:
                continue
        home_away = tds[3].get_text('|', strip=True)
        home = home_away.split('-')[0].strip()
        away = home_away.split('-')[1].strip() 
        
        if find_in_result2(res, prev_date, home, away)==True:
            continue

        if tds[4].find('a', title='Seuranta') == None:
            continue
        link_url = tds[4].find('a', title='Seuranta').get('href')
        link_url = urljoin(url, link_url)
        try:
            driver1.get(link_url)
            ttime.sleep(1)
        except:
            try:
                driver1.get(link_url)
                ttime.sleep(1)
            except:
                driver1.close()
                return -1

        soup1 = BeautifulSoup(driver1.page_source, "html.parser")
        if soup1.find('table')==None:
            continue
        tbody = soup1.find('table').find('tbody')
        if tbody==None:
            continue
        goal_keeper = find_specific_item_with_text(tbody, 'tr', 'period', 'Maalivahdit').find_next_sibling('tr') #soup1.find(class_='period').find(text='Maalivahdit').parent.find_next_sibling()
        item1 = goal_keeper.find_all('td')
        keeper_item1 = item1[0].find('a')
        home_keeper1 = keeper_item1.get_text('|', strip=True)
        store_item1 = keeper_item1.next_sibling
        home_store1 = store_item1.strip() #store_item1.get_text('|', strip=True)
        home_store1 = str(get_pure_store_value(home_store1))
        keeper_item2 = item1[2].find('a')
        away_keeper1 = keeper_item2.get_text('|', strip=True)
        store_item2 = keeper_item2.next_sibling
        away_store1 = store_item2.strip() #.get_text('|', strip=True)        
        away_store1 = str(get_pure_store_value(away_store1))
        goal_keeper = goal_keeper.find_next_sibling('tr')
        home_keeper2 = ''
        home_store2 = ''
        away_keeper2 = ''
        away_store2 = ''
        if goal_keeper['class'][0] == 'even':
            item2 = goal_keeper.find_all('td')
            keeper_item1 = item2[0].find('a')
            if keeper_item1:
                home_keeper2 = keeper_item1.get_text('|', strip=True)
                store_item1 = keeper_item1.next_sibling
                home_store2 = store_item1.strip() #store_item1.get_text('|', strip=True)
                val = get_pure_store_value(home_store2)
                if val != 0:
                    home_store2 = str(val)
            keeper_item2 = item2[2].find('a')
            if keeper_item2:
                away_keeper2 = keeper_item2.get_text('|', strip=True)
                store_item2 = keeper_item2.next_sibling
                away_store2 = store_item2.strip() #.get_text('|', strip=True)        
                val = get_pure_store_value(away_store2)
                if val != 0:
                    away_store2 = str(val)

        if find_specific_item_with_text(tbody, 'tr', 'period', '3. erä'):
            TM = find_specific_item_with_text(tbody, 'tr', 'period', '3. erä').find_next_sibling('tr')
        # TM_home = 0
        # TM_home_str = ''
        # TM_away = 0
        # TM_away_str = ''
        # TM_home_idx = 0
        # TM_away_idx = 0
        TM_home_count = 0
        TM_away_count = 0
        TM_home = ''
        TM_away = ''
        while TM.get_text('|', strip=True) != 'Maalivahdit':
            if TM.find('strong') and TM.find('strong').get_text().find('TM') != -1:
                strong_elem_home = TM.find('td', class_='home').find('strong')
                if strong_elem_home and strong_elem_home.get_text().find('TM') != -1:
                    TM_home_count += 1

                    # TM_user_homes = strong_elem_home.find_next_siblings('a')
                    # if TM_user_homes:
                    #     for TM_user_home in TM_user_homes:
                    #         TM_val_home = TM_user_home.next_sibling.strip("(), \n")
                    #         TM_val_home = TM_val_home.strip()
                    #         TM_home += int(TM_val_home)
                    #         if TM_home_idx > 0:
                    #             TM_home_str += ','
                    #         TM_home_str += TM_val_home
                    #         TM_home_idx += 1
                strong_elem_away = TM.find('td', class_='away').find('strong')
                if strong_elem_away and strong_elem_away.get_text().find('TM') != -1:
                    TM_away_count += 1
                    # TM_user_aways = strong_elem_away.find_next_siblings('a')
                    # if TM_user_aways:
                    #     for TM_user_away in TM_user_aways:
                    #         TM_val_away = TM_user_away.next_sibling.strip("(), \n")
                    #         TM_val_away = TM_val_away.strip()
                    #         TM_away += int(TM_val_away)
                    #         if TM_away_idx > 0:
                    #             TM_away_str += ','
                    #         TM_away_str += TM_val_away
                    #         TM_away_idx += 1

            TM = TM.find_next_sibling('tr')
        if TM_home_count != 0:
            TM_home = str(TM_home_count)
        if TM_away_count != 0:
            TM_away = str(TM_away_count)
        match_res = MatchResult(prev_day, prev_date_string, home, away, home_keeper1, away_keeper1, home_store1, away_store1, home_keeper2, away_keeper2, home_store2, away_store2, TM_home, TM_away, link_url)
        if find_in_result(res, match_res)==False:
            res.append(match_res)
    driver1.close()
    return 0

default_url = ''
def load_select_items():
    driver.set_page_load_timeout(50)
    fp = open("url.txt", "r")
    for url in fp:
        default_url = url
        break
    driver.get(default_url)
    ttime.sleep(2)
    tournaments = []
    option_tournaments = driver.find_element_by_xpath("//select[@name='tournament']").find_elements_by_tag_name("option")
    for option in option_tournaments:
        tournaments.append(option.text)
    seasons = []
    option_season = driver.find_element_by_xpath("//select[@name='season']").find_elements_by_tag_name("option")
    for option in option_season:
        seasons.append(option.text)
    return tournaments, seasons

def close_driver():
    driver.close()

def find_in_result(result, obj):
    for r in result:
        if r.date==obj.date and r.home==obj.home and r.away==obj.away:
            return True
    return False

def find_in_result2(result, date, home, away):
    for r in result:
        if r.date==date and r.home==home and r.away==away:
            return True
    return False

class MatchResult:
    def __init__(self, day, date, home, away, maalivahdit_home1, maalivahdit_away1, torjunnat_home1, torjunnat_away1, maalivahdit_home2, maalivahdit_away2, torjunnat_home2, torjunnat_away2, TM_home, TM_away, url):
        self.day = day
        self.date_string = date
        d, m, y = [int(x) for x in date.split('.')]
        self.date = datetime.date(y, m, d)
        self.home = home
        self.away = away
        self.maalivahdit_home1 = maalivahdit_home1
        self.maalivahdit_away1 = maalivahdit_away1
        self.torjunnat_home1 = torjunnat_home1
        self.torjunnat_away1 = torjunnat_away1
        self.maalivahdit_home2 = maalivahdit_home2
        self.maalivahdit_away2 = maalivahdit_away2
        self.torjunnat_home2 = torjunnat_home2
        self.torjunnat_away2 = torjunnat_away2
        self.TM_home = TM_home
        self.TM_away = TM_away
        self.url = url

def sort_func(e):
    d, m, y = e.date.split('.')
    h = e.home
    return datetime.date(y, m, d), h

def get_match_result(filename, season, date_all_flg, date_from, date_to):
    workbook_match = xlrd.open_workbook(filename)
    worksheet_match = workbook_match.sheet_by_index(0)

    invalid_format = False

    if worksheet_match.ncols != 15:
        invalid_format = True
    else:
        if worksheet_match.cell_value(1, 0) != 'Date':
            invalid_format = True
        if worksheet_match.cell_value(1, 2)!='home' or worksheet_match.cell_value(1, 4)!='home' or worksheet_match.cell_value(1, 6)!='home' or worksheet_match.cell_value(1, 8)!='home' or worksheet_match.cell_value(1, 10)!='home' or worksheet_match.cell_value(1, 12)!='home':
            invalid_format = True
        if worksheet_match.cell_value(1, 3)!='away' or worksheet_match.cell_value(1, 5)!='away' or worksheet_match.cell_value(1, 7)!='away' or worksheet_match.cell_value(1, 9)!='away' or worksheet_match.cell_value(1, 11)!='away' or worksheet_match.cell_value(1, 13)!='away':
            invalid_format = True

    match_res_array = []
    if invalid_format ==  False:
        for row in range(2, worksheet_match.nrows):
            match_res = MatchResult(worksheet_match.cell_value(row,0),worksheet_match.cell_value(row,1),worksheet_match.cell_value(row,2),worksheet_match.cell_value(row,3),
                worksheet_match.cell_value(row,4), worksheet_match.cell_value(row,5), worksheet_match.cell_value(row,6), worksheet_match.cell_value(row,7),
                worksheet_match.cell_value(row,8), worksheet_match.cell_value(row,9), worksheet_match.cell_value(row,10), worksheet_match.cell_value(row,11),
                worksheet_match.cell_value(row,12), worksheet_match.cell_value(row,13), worksheet_match.cell_value(row,14))
            match_res_array.append(match_res)

    workbook_match.release_resources()
    del workbook_match

    fp = open("url.txt", "r")
    r = 0
    for url in fp:
        r = analyse_page2(url, match_res_array, season, date_all_flg, date_from, date_to)
        break

    match_res_array = sorted(match_res_array, key=attrgetter('date', 'home'))
    fp.close()

    global line
    line = 3

    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()
    merge_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': 'white'})

    worksheet.write("A1", "")
    worksheet.write("B1", "")
    worksheet.write("C1", "")
    worksheet.write("D1", "")
    worksheet.merge_range('A2:B2', 'Date', merge_format)
    worksheet.merge_range('E1:F1', 'maalivahdit', merge_format)
    worksheet.merge_range('G1:H1', 'torjunnat', merge_format)
    worksheet.merge_range('I1:J1', 'maalivahdit', merge_format)
    worksheet.merge_range('K1:L1', 'torjunnat', merge_format)
    worksheet.merge_range('M1:N1', 'TM', merge_format)

    worksheet.write("C2", "home")
    worksheet.write("D2", "away")
    worksheet.write("E2", "home")
    worksheet.write("F2", "away")
    worksheet.write("G2", "home")
    worksheet.write("H2", "away")
    worksheet.write("I2", "home")
    worksheet.write("J2", "away")
    worksheet.write("K2", "home")
    worksheet.write("L2", "away")
    worksheet.write("M2", "home")
    worksheet.write("N2", "away")
    worksheet.write("O2", "url")
    for item in match_res_array:
        worksheet.write('A'+str(line), item.day)
        worksheet.write('B'+str(line), item.date_string)
        worksheet.write('C'+str(line), item.home)
        worksheet.write('D'+str(line), item.away)
        worksheet.write('E'+str(line), item.maalivahdit_home1)
        worksheet.write('F'+str(line), item.maalivahdit_away1)
        worksheet.write('G'+str(line), item.torjunnat_home1)
        worksheet.write('H'+str(line), item.torjunnat_away1)
        worksheet.write('I'+str(line), item.maalivahdit_home2)
        worksheet.write('J'+str(line), item.maalivahdit_away2)
        worksheet.write('K'+str(line), item.torjunnat_home2)
        worksheet.write('L'+str(line), item.torjunnat_away2)
        worksheet.write('M'+str(line), item.TM_home)
        worksheet.write('N'+str(line), item.TM_away)
        worksheet.write('O'+str(line), item.url)
        
        line += 1

    # workbook.save(filename)
    workbook.close()
    if r==-1:
        return -2

    return 0

"""
if __name__ == "__main__":
    fp = open("url.txt", "r")
    merge_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': 'white'})

    worksheet.write("A1", "")
    worksheet.write("B1", "")
    worksheet.write("C1", "")
    worksheet.write("D1", "")
    worksheet.merge_range('A2:B2', 'Date', merge_format)
    worksheet.merge_range('E1:F1', 'maalivahdit', merge_format)
    worksheet.merge_range('G1:H1', 'torjunnat', merge_format)
    worksheet.merge_range('I1:J1', 'TM', merge_format)

    worksheet.write("C2", "home")
    worksheet.write("D2", "away")
    worksheet.write("E2", "home")
    worksheet.write("F2", "away")
    worksheet.write("G2", "home")
    worksheet.write("H2", "away")
    worksheet.write("I2", "home")
    worksheet.write("J2", "away")
    worksheet.write("K2", "home")
    worksheet.write("L2", "away")
    worksheet.write("M2", "home")
    worksheet.write("N2", "away")
    worksheet.write("O2", "url")

    driver.set_page_load_timeout(30)
    for url in fp:
        analyse_page1(url)
    fp.close()
"""