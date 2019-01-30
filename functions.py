from time import sleep
from glob import glob
from datetime import datetime
from shutil import move
from os import getcwd
from os.path import expanduser, getctime
from selenium import webdriver

# Open browser
driver = webdriver.Chrome(getcwd() + "/chromedriver")
driver.get('https://facebook.com/login')


def xpath(path, container=None):
    if not container:
        return driver.find_element_by_xpath('//' + path)
    return xpath('//' + container).find_elements_by_xpath('/' + path)


# def wait_for_closed_notification():
#     t_0 = 0
#     while t_0 < 60:
#         try:
#             xpath('a[@title="Profile"]/span').click()
#         except:
#
#
#     if t_0 > 60:
#         return "Unable to download images.  Ending Early"
#     else:
#         try:
#             xpath('a[@title="Profile"]/span').click()
#             # driver.minimize_window()
#         except:
#             sleep(1)
#             return wait_for_closed_notification(t_0 + 1)


def download_image():
    photos = xpath('div[@id="pagelet_timeline_medley_photos"]')
    a = xpath('a[@data-action-type="download_photo"]', container=photos)
    link = a[-1].get_attribute('href') # Get link to download
    driver.get(link)  # Download link
    sleep(1)
    return


def most_recent_file(folder_name):
    folder = expanduser(folder_name + '/*')
    list_of_files = glob(folder)
    file = max(list_of_files, key=getctime)
    return file


def rename_img(i):

    fb_date = xpath('span[@id="fbPhotoSnowliftTimestamp"]/a/abbr').get_attribute('title') # Timestamp of image

    # Shorten string from `Monday, Januaray 31, 2018 at 5:15pm`to `January 31, 2018`
    fb_date = fb_date[fb_date.find(', ')+2: fb_date.find(' at')]

    day_10_digit = fb_date.find(', 20') - 2 # Add 0 to the date string if it's a single-digit # day
    if fb_date[day_10_digit] == ' ':
        fb_date = fb_date[:day_10_digit] + ' 0' + fb_date[day_10_digit+1:]

    img_date_datetime = datetime.strptime(fb_date, '%B %d, %Y') # string type => datetime type
    img_date_string = datetime.strftime(img_date_datetime, '%Y-%m-%d') # datetime object => `2018-01-31`
    img_number = '0' * (4-len(str(i))) + str(i)

    filename = 'Photos-of-You/' + img_number + '-' + img_date_string + '.jpg'
    return filename
