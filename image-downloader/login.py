from threading import Thread
from selenium import webdriver
import time

driver = webdriver.Chrome(executable_path='e:/python/image_download/image-downloader-0.1.1/chromedrive/chromedriver.exe')
driver.implicitly_wait(10)

def login(url, id, pw):
    driver.get(url)
    time.sleep(5)
    elem_button = driver.find_element_by_id('gnb_login_button')
    login_url = elem_button.get_attribute('href')
    driver.get(login_url)
    while True:
        try:
            userid = driver.find_element_by_xpath("//input[@id='id']")
            password = driver.find_element_by_xpath("//input[@id='pw']")
            userid.send_keys(id)
            password.send_keys(pw)
            on = driver.find_element_by_xpath("//input[@class='btn_global'][@type='submit']")
            if not on:
                break
            on.click()
            time.sleep(5)
        except:
            break
    time.sleep(5)




login('https://comic.naver.com/index.nhn', 'kxjer@hotmail.com', 'ewkddf')
