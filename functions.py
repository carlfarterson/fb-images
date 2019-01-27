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


def wait_for_closed_notification(t_0):
    if t_0 > 60:
        return "Unable to download images.  Ending Early"
    else:
        try:
            xpath('a[@title="Profile"]/span').click()
        except:
            sleep(1)
            return wait_for_closed_notification(t_0 + 1)


def main(img_count):
    xpath('span[contains(text(), "Options")]').click() # Click on options
    sleep(1)
    download_image() # download image
    fb_date = xpath('span[@id="fbPhotoSnowliftTimestamp"]/a/abbr').get_attribute('title') # Timestamp of image
    fb_date = validate_date(fb_date)
    try:
        filename, img_count = rename_img(fb_date, img_count)
        move(most_recent_file('~/Downloads'), filename)
        xpath('a[@title="Next"]').click() # Go to next image
        return main(img_count)
    except TypeError as error:
        # Now we can delete the placeholder file
        remove(placeholder)
        remove(most_recent_file('~/Downloads'))
        print("Download complete")
        sleep(10)


def xpath(path, container=None):
    if not container:
        return driver.find_element_by_xpath('//' + path)
    return container.find_elements_by_xpath('//' + path)


def download_image():
    photos = xpath('div[@id="pagelet_timeline_medley_photos"]')
    a = xpath('a[@data-action-type="download_photo"]', container=photos)
    link = a[-1].get_attribute('href') # Get link to download
    driver.get(link)  # Download link
    return


def validate_date(fb_date):
    # Add 0 to the date string if it needs to
    # Otherwise, return the string
    day_10 = fb_date.find(', 20') - 2
    if day_10 == ' ':
        middle = day_10 - 1
        return fb_date[:middle] + '0' + fb_date[middle:]
    else:
        return fb_date


def most_recent_file(folder_name):
    folder = expanduser(folder_name + '/*')
    list_of_files = glob(folder)
    file = max(list_of_files, key=getctime)
    return file


def rename_img(date_string, i):
    date_string_clean = date_string[date_string.find(',')+2:date_string.find(' at')] # Shorten the string to `January 01, 2018`
    img_date = datetime.strptime(date_string_clean, '%B %d, %Y') # string type => datetime type

    last_img = most_recent_file('Photos-of-You')
    last_img_date = datetime.strptime(last_img[last_img.find('/')+1: -8], '%Y-%m-%d')

    if last_img_date.year > img_date.year:
        return

    if last_img_date.day == img_date.day \
        and last_img_date.month == img_date.month \
        and last_img_date.year == img_date.year:
        i += 1
    else:
        i = 1

    img_date_string = datetime.strftime(img_date, '%Y-%m-%d') # datetime object => `2018-01-31`
    filename = 'Photos-of-You/' + img_date_string + '-' + '0'*(3-len(str(i))) + str(i) + '.jpg'
    return filename, i
