from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import random
import time
import pandas as pd
import logging
import os, sys
import urllib
import shutil

def get_hrefs(urls):
    """
    The webpage scrapper for list of all dogs. Design for adoptapet.com
    param:
        url: the list of links to webpage holding dog's infor
    return:
        hrefs: hrefs for all the dogs.
    """
    hrefs = []
    driver = webdriver.Chrome(executable_path="/Users/elainezhao/Desktop/puppylover_test/chromedriver")

    for url in urls:
        driver.get(url)    
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        
        for link in soup.find_all("a", {"class": "pet__item__link"}):
            href = link.get('href')
            hrefs.append('https://www.adoptapet.com' + href)
        
    driver.close()
    return hrefs


def get_photo(hrefs):
    """
    Input: a list of hrefs for different dogs
    Output: list of titles and list of photo urls for those dogs
    """
    titles = []
    photo_urls = []
    driver = webdriver.Chrome(executable_path="/Users/elainezhao/Desktop/puppylover_test/chromedriver")
    for i, href in enumerate(hrefs):
        driver.get(href) # use selenium
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        try:
            title = soup.title.text
            titles.append(title)
        except:
            titles.append(' ')

        try:
            div = soup.find('div', {"data-gallery": "gallery-image"})
            photo_url = div.find('img')['src']
            photo_urls.append(photo_url)
        except:
            photo_urls.append(' ')

    return titles, photo_urls



def download_image(link, name, web_site, path):
    """
    This function is to build a file folder that contains the downloaded picture.
    param:
       link: the list of image url, for which should only be the url.
       name: the name of the sub-directory.
       web_site: the website’s name.
    return:
       Nothing.
    """
    path += name
    # build a folder
    if os.path.exists(path):
        shutil.rmtree(path)
    try:
        os.mkdir(path)
    except OSError:
        logging.info("Creation of the directory %s failed" % path)
    # iterate through all url link
    for i, url in enumerate(link):
        # save the image
        request = urllib.request.Request(
            url, headers={'User-Agent': 'Mozilla/5.0'})
        img_name = str(i)+".jpg"
        with urllib.request.urlopen(request) as response, open(path+"/"+img_name, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
    # return a notice.
    logging.info("Store all images from link.")


def get_urls(url):
    urls = []
    for i in range(1, 3):
        urls.append(url + f'&page={i}#')
    return urls



def main():
    url = str(sys.argv[1])
    print(url)
    urls = get_urls(url)
    hrefs = get_hrefs(urls)
    name = 'adoptapet'
    web_site = 'adoptapet'
    path = '/Users/elainezhao/Desktop/dog_img'

    titles, photo_urls = get_photo(hrefs)
    df = pd.DataFrame({'links': hrefs, 'titles': titles, 'photo_url': photo_urls})
    df = df[df.photo_url != ' '].reset_index()
    df.to_csv('adoptapet.csv', index=False)
    download_image(df.photo_url, name, web_site, path)


if __name__ == "__main__":
    # execute only if run as a script
    main()
