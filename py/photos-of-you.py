import random
import asyncio
from decimal import Decimal
from time import sleep
from glob import glob
from datetime import datetime
from shutil import move
from os import getcwd
from os.path import expanduser, getctime
from selenium import webdriver

SLEEP_INTERVAL = 0.1

# Open browser
driver = webdriver.Chrome(getcwd() + "/chromedriver")
driver.get('https://facebook.com/login')

# Log in
login, password = pd.read_csv('login.csv').values[0]
async_send_keys('input[@id="email"]')
async_send_keys('input[@id="pass"]')
async_click('button[@id="loginbutton"]')

# Click on profile
async_click('a[@title="Profile"]/span')

# Hide window
# driver.minimize_window()

# Go to photos
async_click('a[contains(text(), "Photos")]')

# Click on first image
xpath('div[@class="tagWrapper"]').click()

# Make directory
makedirs('Photos-of-You')





# Functions
def xpath(path, container=None):
    if not container:
        return driver.find_element_by_xpath('//' + path)
    else:
        return xpath('//' + container).find_elements_by_xpath('/' + path)

def async_send_keys(path, val, x=0):
    if x > 600:
        return 'Failed after 60 seconds.  Aborting early.'
    else:
        try:
            xpath(path).send_keys(val)
        except:
            sleep(SLEEP_INTERVAL)
            return send_keys(path, val, x+1)

def async_click(path, x=0):
    if x > 600:
        return 'Failed after 60 seconds.  Aborting early.'
    else:
        try:
            xpath(path).click()
        except:
            sleep(SLEEP_INTERVAL)
            return async_click(path, x+1)
