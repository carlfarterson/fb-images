import os
import requests
from urllib.request import urlretrieve
from datetime import datetime
import numpy as np
import pandas as pd
from selenium import webdriver

login, password = pd.read_csv('login.csv').values[0]
driver = webdriver.Chrome(executable_path="/home/carter/Documents/github/chromedriver")

def xpath(path, container=None):
    if not container:
        return driver.find_element_by_xpath('//' + path)
    return container.find_element_by_xpath('//' + path)


driver.get('https://facebook.com/login')

# Log in to Facebook
xpath('input[@id="email"]').send_keys(login)
xpath('input[@id="pass"]').send_keys(password)
xpath('button[@id="loginbutton"]').click()

# Click on profile
xpath('a[@title="Profile"]/span').click()
# Go to photos
xpath('a[contains(text(), "Photos")]').click()
photos = xpath('div[@id="pagelet_timeline_medley_photos"]')

''' Download 'Photos of You' '''

style = xpath('div[@class="tagWrapper"][1]/i').get_attribute('style')
start = style.find('url')
end = style.find('.jpg')
url = style[start+5:end] + '.jpg'
urlretrieve(url, 'test.jpg')
'71.0.3578.98'

s = requests.session()
s.headers.update({'User-Agent': 'Chrome/71.0.3578.98'})


[s.cookies.update({cookie['name']: cookie['value']})
 for cookie in driver.get_cookies()]

r = s.get(url, allow_redirects=True)
