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
from util_scripts.evaluation import *


class Test_evaluation():    
    def test_(self):
        folder_path = '/Users/elainezhao/Desktop/evaluate_all/'
        accuracy_efficientnetb3 = evaluate("efficientnetb3", folder_path)
        accuracy_vgg = evaluate("vgg", folder_path)
        accuracy_resnet = evaluate("resnet", folder_path)
        accuracy_inception = evaluate("inception", folder_path)
        accuracy_efficientnetb0 = evaluate("efficientnetb0", folder_path)
        
        assert np.round(accuracy_inception, 2) > 0
        assert np.round(accuracy_vgg, 2) > 0
        assert np.round(accuracy_efficientnetb0, 2) > 0
        assert np.round(accuracy_efficientnetb3, 2) > 0
        assert np.round(accuracy_resnet, 2) > 0
                 