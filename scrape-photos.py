from os import remove
from os.path import expanduser, getctime
from shutil import move
import glob
from PIL import Image
from datetime import datetime
import numpy as np
import pandas as pd
from selenium import webdriver


login, password = pd.read_csv('login.csv').values[0]
driver = webdriver.Chrome(executable_path="/home/carter/Documents/github/chromedriver")

def xpath(path, container=None):
    if not container:
        return driver.find_element_by_xpath('//' + path)
    return container.find_elements_by_xpath('//' + path)


driver.get('https://facebook.com/login')

# Log in to Facebook
xpath('input[@id="email"]').send_keys(login)
xpath('input[@id="pass"]').send_keys(password)
xpath('button[@id="loginbutton"]').click()
# NOTE: need to click to disable notifications

# Click on profile
xpath('a[@title="Profile"]/span').click()
# Go to photos
xpath('a[contains(text(), "Photos")]').click()
photos = xpath('div[@id="pagelet_timeline_medley_photos"]')

''' Download 'Photos of You' '''

xpath('div[@class="tagWrapper"]').click() # click on first image
xpath('a[@title="Next"]').click() # Go to next image
xpath('span[contains(text(), "Options")]').click() # Click on options
download_link = xpath('a[@data-action-type="download_photo"]', photos)[-1].get_attribute('href') # Get link to download
driver.get(download_link)  # Download link



# ------------------------------------------------------------------------------
# Testing
date = xpath('span[@id="fbPhotoSnowliftTimestamp"]/a/abbr').get_attribute('title')
date_string = date[date.find(',')+2:date.find(' at')]
date_date = datetime.strptime(date_string, '%B %d, %Y')
date_string_new = datetime.strftime(date_date, '%Y-%m-%d')
# NOTE: we'll add three 0's before .jpg, just in case >100 images were uploaded in a day

downloads_folder = expanduser('~/Downloads/*')
list_of_files = glob.glob(downloads_folder)
latest_file = max(list_of_files, key=getctime)

img = Image.open(latest_file)
img.show()








# ------------------------------------------------------------------------------
