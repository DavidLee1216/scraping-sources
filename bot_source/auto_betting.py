import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import datetime
import time as ttime
import xlsxwriter
import xlrd
from os.path import isfile

user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/63.0.3239.84 Chrome/63.0.3239.84 Safari/537.36'

python_version = sys.version_info.major

MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

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

def get_excel_sheet_object(fname, idx=0):
    if not isfile(fname):
        return 0

    # Open the workbook and 1st sheet
    xl_workbook = xlrd.open_workbook(fname)
    xl_sheet = xl_workbook.sheet_by_index(idx)
    
    return xl_sheet

def login(driver, url, username, password):
    driver.get(url)
    user_field = driver.find_element_by_xpath("//div[@class='user-box']/div[@class='anonymous-only']")
    css_val = user_field.value_of_css_property("display")
    if 'block' in css_val:
        username_field = driver.find_element_by_xpath("//div[@class='form-field identifier']/input[@id='connection_login']")
        if username_field:
            password_field = driver.find_element_by_xpath("//div[@class='form-field password']/input[@id='connection_password']")
            if password_field:
                username_field.clear()
                password_field.clear()
                username_field.send_keys(username)
                password_field.send_keys(password)
                login_button = driver.find_element_by_xpath("//button[@id='connection_submit']")
                driver.execute_script("arguments[0].click();", login_button)
                ttime.sleep(2)
                user_field = driver.find_element_by_xpath("//div[@class='user-box']/div[@class='anonymous-only']")
                css_val = user_field.value_of_css_property("display")
                if 'block' in css_val:
                    return False
    return True

def selectBettingType(driver, url, bet_type):
    if bet_type=='SG':
        try:
            betting_type_item = driver.find_element_by_xpath("//button[@class='chk-change-pari paris-arrondi_79x40_1']")
            if betting_type_item:
                betting_type_item.click()
                ttime.sleep(0.1)
                return True
        except:
            return False
    elif bet_type=='SP':
        try:
            betting_type_item = driver.find_element_by_xpath("//button[@class='chk-change-pari paris-arrondi_79x40_2']")
            if betting_type_item:
                betting_type_item.click()
                ttime.sleep(0.1)
                return True
        except:
            return False
    elif bet_type=='ZS':
        try:
            betting_type_item = driver.find_element_by_xpath("//button[@class='chk-change-pari paris-arrondi_79x40_29']")
            if betting_type_item:
                betting_type_item.click()
                ttime.sleep(0.1)
                return True
        except:
            return False
    elif bet_type=='ZC':
        try:
            betting_type_item = driver.find_element_by_xpath("//button[@class='chk-change-pari paris-arrondi_79x40_7']")
            if betting_type_item:
                betting_type_item.click()
                ttime.sleep(0.1)
                return True
        except:
            return False
    elif bet_type=='JG':
        try:
            betting_type_item = driver.find_element_by_xpath("//button[@class='chk-change-pari paris-arrondi_79x40_3']")
            if betting_type_item:
                betting_type_item.click()
                ttime.sleep(0.05)
                reduce_items = driver.find_elements_by_xpath("//div[@class='tabs-menu typecombine']/button")
                if reduce_items[1]:
                    driver.execute_script("arguments[0].click();", reduce_items[1])
                ttime.sleep(0.05)
                return True
        except:
            return False
    elif bet_type=='JP':
        try:
            betting_type_item = driver.find_element_by_xpath("//button[@class='chk-change-pari paris-arrondi_79x40_5']")
            if betting_type_item:
                betting_type_item.click()
                ttime.sleep(0.05)
                reduce_items = driver.find_elements_by_xpath("//div[@class='tabs-menu typecombine']/button")
                if reduce_items[1]:
                    driver.execute_script("arguments[0].click();", reduce_items[1])
                ttime.sleep(0.05)
                return True
        except:
            return False
    else:
        try:
            if bet_type=='JU':
                path_str = "//button[@class='chk-change-pari paris-arrondi_79x40_4']"
            elif bet_type=='Z2/4':
                path_str = "//button[@class='chk-change-pari paris-arrondi_79x40_13']"
            elif bet_type=='TR':
                path_str = "//button[@class='chk-change-pari paris-arrondi_79x40_6']"
            elif bet_type=='TRI':
                path_str = "//button[@class='chk-change-pari paris-arrondi_79x40_11']"
            betting_type_item = driver.find_element_by_xpath(path_str)
            if betting_type_item:
                betting_type_item.click()
                ttime.sleep(0.05)
                reduce_items = driver.find_elements_by_xpath("//div[@class='tabs-menu typecombine']/button")
                if reduce_items[1]:
                    driver.execute_script("arguments[0].click();", reduce_items[1])
                ttime.sleep(0.05)
                return True
        except:
            return False
    return False

def selectCombination(driver, url, combination, bet_type):
    if bet_type=='SG' or bet_type=='SP' or bet_type=='ZS' or bet_type=='ZC':
        try:
            path_str = "//tbody/tr[@data-runner='{:d}']".format(combination)
            comb_item = driver.find_element_by_xpath(path_str)
            if comb_item:
                if bet_type=='SG':
                    path_str = "//tbody/tr[@data-runner='{:d}']/td[@class='gagnant']/button[@title='G']".format(combination)
                elif bet_type=='SP':
                    path_str = "//tbody/tr[@data-runner='{:d}']/td[@class='place']/button[@title='P']".format(combination)
                elif bet_type=='ZS':
                    path_str = "//tbody/tr[@data-runner='{:d}']/td[@class='selection']/button[@title='S']".format(combination)
                elif bet_type=='ZC':
                    path_str = "//tbody/tr[@data-runner='{:d}']/td[@class='selection']/button[@title='S']".format(combination)
                G_item = driver.find_element_by_xpath(path_str)
                G_item.click()
                ttime.sleep(0.1)
        except:
            return False
    elif bet_type=='JG' or bet_type=='JP' or bet_type=='JU' or bet_type=='Z2/4':
        try:
            winners = combination.split('/', 1)
            if len(winners)<2:
                return False
            main_winner = int(winners[0].strip())
            combinate_str_winners = winners[1].split(',')
            path_str = "//tbody/tr[@data-runner='{:d}']/td[@class='base']/button[@title='B']".format(main_winner)
            B_item = driver.find_element_by_xpath(path_str)
            B_item.click()
            ttime.sleep(0.1)
            for comb_winner in combinate_str_winners:
                winner = int(comb_winner.strip())
                if winner==main_winner:
                    continue
                path_str = "//tbody/tr[@data-runner='{:d}']/td[@class='combine']/button[@title='C']".format(winner)
                C_item = driver.find_element_by_xpath(path_str)
                C_item.click()
                ttime.sleep(0.1)
        except:
            return False
    elif bet_type=='TR':
        try:
            winners = combination.split('/', 1)
            if len(winners) < 2:
                return False
            main_str_winners = winners[0].split(',')
            if len(main_str_winners) > 2:
                return False
            main_winners = []
            for main_str_winner in main_str_winners:
                main_winners.append(int(main_str_winner.strip()))
            for main_winner in main_winners:
                path_str = "//tbody/tr[@data-runner='{:d}']/td[@class='base']/button[@title='B']".format(main_winner)
                B_item = driver.find_element_by_xpath(path_str)
                B_item.click()
                ttime.sleep(0.05)
            combinate_str_winners = winners[1].split(',')
            for comb_winner in combinate_str_winners:
                winner = int(comb_winner.strip())
                if winner in main_winners:
                    continue
                path_str = "//tbody/tr[@data-runner='{:d}']/td[@class='combine']/button[@title='C']".format(winner)
                C_item = driver.find_element_by_xpath(path_str)
                C_item.click()
                ttime.sleep(0.05)
        except:
            return False
    elif bet_type=='TRI':
        try:
            winners = combination.split('/', 2)
            if len(winners) < 3:
                return False
            first_winner = int(winners[0].strip())
            second_winner = int(winners[1].strip())
            path_str = "//tbody/tr[@data-runner='{:d}']/td[@class='base']/button[@title='B']".format(first_winner)
            B_item = driver.find_element_by_xpath(path_str)
            B_item.click()
            path_str = "//tbody/tr[@data-runner='{:d}']/td[@class='base']/button[@title='B']".format(second_winner)
            B_item = driver.find_element_by_xpath(path_str)
            B_item.click()
            combinate_str_winners = winners[2].split(',')
            for comb_winner in combinate_str_winners:
                winner = int(comb_winner.strip())
                if winner==first_winner or winner==second_winner:
                    continue
                path_str = "//tbody/tr[@data-runner='{:d}']/td[@class='combine']/button[@title='C']".format(winner)
                C_item = driver.find_element_by_xpath(path_str)
                C_item.click()
                ttime.sleep(0.05)
        except:
            return False

def checkStakeBetType(class_name, bet_type):
    if class_name=='recap-picto paris-carre_30x25_1' and bet_type=='SG':
        return True
    elif class_name=='recap-picto paris-carre_30x25_2' and bet_type=='SP':
        return True
    elif class_name=='recap-picto paris-carre_30x25_29' and bet_type=='ZS':
        return True
    elif class_name=='recap-picto paris-carre_30x25_7' and bet_type=='ZC':
        return True
    elif class_name=='recap-picto paris-carre_30x25_3' and bet_type=='JG':
        return True
    elif class_name=='recap-picto paris-carre_30x25_5' and bet_type=='JP':
        return True
    elif class_name=='recap-picto paris-carre_30x25_4' and bet_type=='JU':
        return True
    elif class_name=='recap-picto paris-carre_30x25_6' and bet_type=='TR':
        return True
    elif class_name=='recap-picto paris-carre_30x25_11' and bet_type=='TRI':
        return True
    elif class_name=='recap-picto paris-carre_30x25_13' and bet_type=='Z2/4':
        return True
    return False

def setStake(driver, stake, bet_type):
    try:
        if bet_type=='SG' or bet_type=='SP' or bet_type=='ZS' or bet_type=='ZC':
            path_str = "//ul[@class='recap-list']/li[@class='pari-simple']"
        elif bet_type=='JG' or bet_type=='JP' or bet_type=='JU' or bet_type=='TR' or bet_type=='TRI' or bet_type=='Z2/4':
            path_str = "//ul[@class='recap-list']/li[@class='pari-complexe']"
        stake_items = driver.find_elements_by_xpath(path_str)
        for stake_item in stake_items:
            path_str = "//div[@class='recap-combi-wrapper']/span"
            item_classname = stake_item.find_element_by_xpath(path_str).get_attribute("class")
            if checkStakeBetType(item_classname, bet_type):
                path_str = "//div[@class='recap-mise-wrapper']/span[@class='recap-mise currency-euro']/input[@class='montant']"
                stake_value_item = stake_item.find_element_by_xpath(path_str)
                stake_value_item.clear()
                ttime.sleep(0.01)
                if bet_type != 'TRI':
                    stake_value_item.send_keys(int(stake))
                else:
                    stake_value_item.send_keys(str(stake))
        return True
    except:
        return False

def logout(driver):
    try:
        close_button = driver.find_element_by_xpath("//div[@class='logged-only']/a[@class='logout tooltip']/i")
        if close_button:
            close_button.click()
    except:
        pass

def clickValidateAndAddToCart(driver, url):
    try:
        path_str = "//div[@class='buttonContainer']/button[@class='validate']"
        validate_item = driver.find_element_by_xpath(path_str)
        validate_item.click()
        ttime.sleep(0.01)
        path_str = "//div[@class='bloc modalValidationSansPanier']/div[@class='footer']/div[@class='btn close']/button[@class='label']"
        confirm_item = driver.find_element_by_xpath(path_str)
        if confirm_item.text=='Confirm':
            confirm_item.click()

        # path_str = "//div[@class='buttonContainer']/button[@class='cart']"
        # addToCardItem = driver.find_element_by_xpath(path_str)
        # addToCardItem.click()
        # ttime.sleep(0.01)
        return True
    except:
        return False

def bet(driver, excel_file):
    sheet = get_excel_sheet_object(excel_file)
    for row_idx in range(1, sheet.nrows):
        url = sheet.cell(row_idx, 0).value
        bet_type = sheet.cell(row_idx, 1).value
        combination = sheet.cell(row_idx, 2).value
        if type(combination) is float:
            combination = int(combination)
        stake = sheet.cell(row_idx, 3).value
        driver.get(url)
        selectBettingType(driver, url, bet_type)
        selectCombination(driver, url, combination, bet_type)
        setStake(driver, stake, bet_type)
        clickValidateAndAddToCart(driver, url)
        ttime.sleep(0.5)
    

if __name__ == "__main__":
    driver = webdriver.Chrome(executable_path='./chromedrive/chromedriver.exe')
    driver.maximize_window()
    driver.set_page_load_timeout(50)
    url = "https://www.zeturf.com/en/course/2020-05-16/R3C8-strasbourg-prix-alexandre-le-grand/turf"
#    bSucc = login(driver, url, "Silverhawk", "Heiwes88!")
