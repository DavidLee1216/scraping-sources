#! /usr/bin/env python3
import csv
import shutil
import sys
import time
import os
import logging
from lxml import html
from bs4 import BeautifulSoup
import re
import gc
import requests
from urllib import request
import urllib
from multiprocessing import Process
from threading import Thread
import psutil


# http client configuration
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/63.0.3239.84 Chrome/63.0.3239.84 Safari/537.36'

# logging configuration
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

python_version = sys.version_info.major
logging.info("executed by python %d" % python_version)

logfile = open('logfile.txt', 'r+')

# compatability with python 2
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
#else:
 #   import urlparse
 #   import urllib
 #   urljoin = urlparse.urljoin
 #   urlretrieve = urllib.urlretrieve
 #   quote = urllib.quote

    # configure headers
 #   class AppURLopener(urllib.FancyURLopener):
 #       version = user_agent
 #   urllib._urlopener = AppURLopener()


def print_state(str, substr):
    print(str + substr)

def fix_url(url):
    url_new = quote(url, safe="%/:=&?~#+!$,;'@()*[]")
    return url_new

PROCESS = psutil.Process(os.getpid())

def print_memory_usage():
    total, available, percent, used, free = psutil.virtual_memory()
    proc =  PROCESS.memory_info()[1]
    print('process=%s total=%s avaliable=%s used=%s free=%s percent=%s' % (proc, total, available, used, free, percent))

def download_row_images(url, dest_dir):
    start_url = url 
    try:
        print_memory_usage()
        img_open =  requests.request('get', url)
        content = img_open.content
        soup = BeautifulSoup(content, "html.parser")
        del content
        for link in soup.find(class_="wt_viewer").find_all("img"):
            image_url = link.get('src')
            image_filename = image_url.rsplit("/", 1)
            image_url = urljoin(start_url, image_url)
            res = download_image_write_requests(image_url, dest_dir, image_filename[1])
            if not res:
                return False
        return True
    except urllib.request.HTTPError as e:
        logging.warning("have trouble to open url. %s" % e)
        return False
    except MemoryError as e:
        logging.warning("have trouble to open url. %s" % e)
        return False
    except Exception as e:
        logging.warning("have trouble to open url. %s" % e)
        return False

def download_image(image_url, dest_dir, image_filename):

    image_url = fix_url(image_url)

    try:
        logging.info("downloading image %s" % image_url)
        tmp_file_name, headers = urlretrieve(image_url)

        image_path = os.path.join(dest_dir, image_filename) #+"."+ext
        if not os.path.exists(image_path):
            shutil.move(tmp_file_name, image_path)
        else:
            pass
        return True
    except urllib.request.HTTPError as e:
        logging.warning("Image download error. %s" % e)
        return False
    except MemoryError as e:
        logging.warning("Image download Memory error. %s" % e)
        return False

def download_image_write(image_url, dest_dir, image_filename):

    image_url = fix_url(image_url)
    image_path = os.path.join(dest_dir, image_filename) #+"."+ext
    print_memory_usage()
    if os.path.exists(image_path):
        return True
    try:
        print_state("downloading image " , image_url)
        img_open = urllib.request.urlopen(image_url) #, context=ssl_context
        print_memory_usage()
        img_content = img_open.read()
        copied_image = open(image_path, "wb")

#        while True:
#            tmp = img_open.read(1024*1024)
#            if not tmp:
#                break
#            copied_image.write(tmp)
#            del tmp

        copied_image.write(img_content)
        del img_content

        copied_image.close()
        img_open.close()
        gc.collect()
        print_memory_usage()
        return True
    except urllib.request.HTTPError as e:
        logging.warning("Image download error. %s" % e)
        return False
    except MemoryError as e:
        logging.warning("Image download Memory error. %s" % e)
        return False
    except Exception as e:
        logging.warning("Image download Exception %s" %e)
        return False

def download_image_write_requests(image_url, dest_dir, image_filename):

    image_url = fix_url(image_url)
    if len(image_filename) > 30:
        image_filename = image_filename[-30:]
    image_path = os.path.join(dest_dir, image_filename) #+"."+ext
    if os.path.exists(image_path):
        return True
    try:
        img_open =  requests.request('get', image_url)
        img_content = img_open.content
        copied_image = open(image_path, "wb")

        copied_image.write(bytes(img_content))
        del img_content

        copied_image.close()
        img_open.close()
        gc.collect()
        return True
    except urllib.request.HTTPError as e:
        os.remove(image_path)
        logging.warning("Image download error. %s" % e)
        return False
    except MemoryError as e:
        os.remove(image_path)
        logging.warning("Image download Memory error. %s" % e)
        return False
    except Exception as e:
        os.remove(image_path)
        logging.warning("Image download Exception %s" %e)
        return False

def download_image_cookie(image_url, dest_dir, image_filename):
    cookies = request.HTTPCookieProcessor()
    opener = request.build_opener(cookies)
    request.install_opener(opener)

    req = request.urlopen(image_url)
    uri = req.url
    response = requests.get(uri)

    if response.status_code == 200:
        with open(os.path.join(dest_dir, image_filename), 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024 * 1024 * 8):
                f.write(chunk)
                return True

    elif response.status_code > 399:
        logging.warning("Image download error.")
        return False
 

"""
format_list = ["jpg", "png", "gif", "svg", "jpeg"]

def process_links(links):
    x = []
    for l in links:
        if os.path.splitext(l)[1][1:].strip().lower() in format_list:
            x.append(l)
    return x

def get_img_list():
    tree = html.fromstring(page_html)
    img = tree.xpath('//img/@src')
    links = tree.xpath('//a/@href')
    img_list = self.process_links(img)
    img_links = self.process_links(links)
    img_list.extend(img_links)
    images = [urljoin(self.url, img_url) for img_url in img_list]
    images = list(set(images))
    self.images = images
    if self.scrape_reverse:
        self.images.reverse()
    return self.images
"""
def cleanString(str):
    text = re.sub('[-=+,#/r\\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', str).strip()
    return text

def get_sub_image_dir(curr_dir, sub_dir):
    new_sub_dir = cleanString(sub_dir)
    dir = curr_dir + "/" + new_sub_dir
    if not os.path.exists(dir):
        os.makedirs(dir)
    return dir

def get_sub_item_urls(url, dest_dir):
    try:
        img_open =  requests.request('get', url)
        content = img_open.content
        soup = BeautifulSoup(content, "html.parser")
        del content
        for link in soup.find(class_="viewList").find_all(class_="title"):
            sub_link_url = link.find("a").get('href')
            sub_link_url = urljoin(url, sub_link_url)
            substr = link.find('a').get_text()
            dir = get_sub_image_dir(dest_dir, substr)
            del link
            while True:
                res = download_row_images(sub_link_url, dir)
                if res:
                    break
                time.sleep(2)
        del soup
        return True
    except Exception as e:
        logging.warning("get_sub_item_urls: %s" % e)
        return False

def get_sub_page_nav_urls(url, dest_dir):
    try:
        img_open =  requests.request('get', url)
        content = img_open.content
        soup = BeautifulSoup(content, "html.parser")
        del content
        res = get_sub_item_urls(url, dest_dir)
        if not res:
            return False
        curr_page = soup.find(class_="page_wrap").find("strong", class_="page")
        next_page = curr_page.find_next_sibling('a')
        del soup
        del curr_page
        if next_page:
            next_url = next_page.get('href')
            del next_page
            next_url = urljoin(url, next_url)
            res = get_sub_page_nav_urls(next_url, dest_dir)
            if not res:
                return False
        return True
    except Exception as e:
        logging.warning("get_sub_page_nav_urls: %s" % e)
        return False

def get_sub_menu_item_webtoon(url, dest_dir):
    try:
        img_open =  requests.request('get', url)
        content = img_open.content
        soup = BeautifulSoup(content, "html.parser")
        del content
        for link in soup.find(class_="list_area daily_all").find_all('img'):
            sub_link_url = link.parent.get('href')
            sub_link_url = urljoin(url, sub_link_url)
            dir = get_sub_image_dir(dest_dir, link.get('title'))
            del link
            res = get_sub_page_nav_urls(sub_link_url, dir)
            if not res:
                return False
        del soup
        return True
    except Exception as e:
        logging.warning("get_sub_menu_item_webtoon: %s" % e)
        return False

def get_sub_menu_item_challenge(url, dest_dir):
    try:
        img_open =  requests.request('get', url)
        content = img_open.content
        soup = BeautifulSoup(content, "html.parser")
        del content
        for link1 in soup.find_all(class_="weekchallengeBox"):
            for link2 in link1.find_all('img'):
                sub_link_url = link2.parent.get('href')
                sub_link_url = urljoin(url, sub_link_url)
                if not link2.get('title'):
                    continue
                dir = get_sub_image_dir(dest_dir, link2.get('title'))
                del link2
                res = get_sub_page_nav_urls(sub_link_url, dir)
                if not res:
                    return False
            del link1
        curr_page = soup.find(class_="page_wrap").find("strong", class_='page')
        next_page = curr_page.find_next_sibling('a')
        if next_page:
            next_url = next_page.get('href')
            next_url = urljoin(url, next_url)
            del curr_page
            del next_page
            res = get_sub_menu_item_challenge(next_url, dest_dir)
            if not res:
                return False
        del soup
        return True
    except Exception as e:
        logging.warning("get_sub_menu_item_challenge: %s" % e)
        return False


def start_menu_urls(url, dest_dir):
    try:

        logfile.seek(0, 2)
        len = logfile.tell()
        logfile.seek(0, 0)
        if len > 0:
            menuId = int(logfile.read(1))
        else:
            menuId = 1
        img_open =  requests.request('get', url)
        content = img_open.content
        soup = BeautifulSoup(content, "html.parser")
        del content
        i = menuId
        for menu in soup.find(class_="menu").find_all("a")[menuId:4]:
            sub_link_url = menu.get("href")
            sub_link_url = urljoin(url, sub_link_url)
            logfile.seek(0, 0)
            logfile.write(str(i))
            logfile.flush()
            if i == 1:
                dir = get_sub_image_dir(dest_dir, menu.get_text())
                res = get_sub_menu_item_webtoon(sub_link_url, dir)
                if not res:
                    return False
            elif i == 2 or i == 3:
                dir = get_sub_image_dir(dest_dir, menu.get_text())
                res = get_sub_menu_item_challenge(sub_link_url, dir)
                if not res:
                    return False
            i = i + 1
        del soup
        return True
    except Exception as e:
        logging.warning("start_menu_urls: %s" % e)
        return False

def get_csv_image_dir(csv_filename):

    base = os.path.basename(csv_filename)
    dir = os.path.splitext(base)[0]

    if not os.path.exists(dir):
        os.makedirs(dir)

    return dir

def download_csv_file_images(filename):

    logging.info("importing data from %s" % filename)

    dest_dir = get_csv_image_dir(filename)
    #check whether csv file has utf-8 bom char at the beginning
    skip_utf8_seek = 0
    with open(filename, "rb") as csvfile:
        csv_start = csvfile.read(3)
        if csv_start == b'\xef\xbb\xbf':
            skip_utf8_seek = 3

    with open(filename, "r") as csvfile:
        # remove ut-8 bon sig
        csvfile.seek(skip_utf8_seek)

        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            res = start_menu_urls(row['url'], dest_dir)
            if not res:
                return False
        return True

def main(args):
    # filename passde through args
    csv_filename = args #[1]
    p = Thread(target=download_csv_file_images, args=(csv_filename,))
    p.start()
#    res = download_csv_file_images(csv_filename)
    while True: #not res:
        time.sleep(20)
        p.join(30)
        if not p.is_alive():
            p = Thread(target=download_csv_file_images, args=(csv_filename,))
            p.start()
#        download_csv_file_images(csv_filename)

#if __name__ == '__main__':
#    main(sys.argv)
#main(sys.argv)
