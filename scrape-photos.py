from os import makedirs
from os.path import expanduser, getctime
from shutil import move
from glob import glob
from PIL import Image
from datetime import datetime
import numpy as np
import pandas as pd
from selenium import webdriver


downloads_folder = expanduser('~/Downloads/*')
login, password = pd.read_csv('login.csv').values[0]
driver = webdriver.Chrome("chromedriver")

def new_image():
    list_of_files = glob(downloads_folder)
    return max(list_of_files, key=getctime)


def xpath(path, container=None):
    if not container:
        return driver.find_element_by_xpath('//' + path)
    return container.find_elements_by_xpath('//' + path)


def rename_img(date_string, i):
    # TODO: are single number days padded??
    date_string_clean = date_string[date_string.find(',')+2:date_string.find(' at')] # Shorten the string to `January 01, 2018`
    date = datetime.strptime(date_string_clean, '%B %d, %Y') # string type => datetime type
    img_date = datetime.strftime(date, '%Y-%m-%d') # datetime object => `2018-01-31`
    img = 'Photos-of-You/' + img_date + '-' + '0'*(4-len(str(i))) + '.jpg'

    if img.exists():
        return rename_img(date_string, i+1)
    else:
        return img, i



# Log in to Facebook
driver.get('https://facebook.com/login')
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

makedirs('Photos-of-You') # Make folder
xpath('div[@class="tagWrapper"]').click() # click on first image
photo_count = 1

while True:

    xpath('span[contains(text(), "Options")]').click() # Click on options
    download_link = xpath('a[@data-action-type="download_photo"]', photos)[-1].get_attribute('href') # Get link to download
    driver.get(download_link)  # Download link

    fb_date = xpath('span[@id="fbPhotoSnowliftTimestamp"]/a/abbr').get_attribute('title') # Timestamp of image
    img_name, photo_count = rename_img(fb_date, photo_count)

    move(new_image(), img_name)


    try:
        xpath('a[@title="Next"]').click() # Go to next image
    except
        pass # Reached end of images



# ------------------------------------------------------------------------------
# Testing



# ------------------------------------------------------------------------------
