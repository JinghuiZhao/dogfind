import sys, os
sys.path.append('../')
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import random
import time
import pandas as pd
import logging
import urllib
import shutil
from util_scripts.web_scrape import *


class Test_web_scrape():    
    def test_web_scrape(self):
        url = 'https://www.adoptapet.com/pet-search?clan_id=1&geo_range=50&location=seattle,%20wa'
        name = 'adoptapet'
        web_site = 'adoptapet'
        path = '/Users/elainezhao/Desktop/dog_img/'

        urls = get_urls(url)
        hrefs = get_hrefs(urls)
        titles, photo_urls = get_photo(hrefs)
        df = pd.DataFrame({'links': hrefs, 'titles': titles, 'photo_url': photo_urls})
        df = df[df.photo_url != ' '].reset_index()
        df.to_csv('adoptapet.csv', index=False)
        download_image(df.photo_url, name, web_site, path)
        assert len(urls) == 2
        assert len(hrefs) == 42
        assert os.path.exists('adoptapet.csv')
        assert len(os.listdir('/Users/elainezhao/Desktop/dog_img/adoptapet')) == len(df)
        
        
