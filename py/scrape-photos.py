from os import makedirs, remove
from shutil import move
from time import sleep
import numpy as np
import pandas as pd
from functions import *

def main(img_count=None, first_img=None):

    await_click('span[contains(text(), "Options")]')
    driver.minimize_window()

    # navigate to profile and get profile username
    await_click('a[@title="Profile"]/span')

    # with facebook.com/username as f
    facebook = 'https://www.facebook.com/'
    url = driver.current_url
    # username = url[url.find('.com/') + 5:] # Do I really need username?

    # 1. Photos of You
    def Photos_of_You():
        driver.get(url + '/photos_of')
        await_click('div[@class="tagWrapper"]')

    pause()
    download_image() # download image
    pause()
    if first_img is None:
        # Get the name of the first file downloaded to ensure we're not downloading
        # another file w/ the same name.
        file = most_recent_file('~/Downloads')
        first_img = file[file.find('Downloads/')+10:file.find('.jpg')]
    elif first_img in most_recent_file('~/Downloads'):
        remove(most_recent_file('~/Downloads'))
        print('Download complete.')
        driver.close()
        sleep(15)
        return

    # continue with main loop
    filename = rename_img(img_count)
    move(most_recent_file('~/Downloads'), filename)
    xpath('a[@title="Next"]').click() # Go to next image
    pause()
    return main(img_count + 1, first_img)


if __name__ == '__main__':

    login, password = pd.read_csv('login.csv').values[0]
    first_img = None

    # Log in to Facebook
    xpath('input[@id="email"]').send_keys(login)
    xpath('input[@id="pass"]').send_keys(password)
    xpath('button[@id="loginbutton"]').click()

    # Click on profile
    t_0 = 0
    async(t_0)
    # Go to photos
    sleep(2)
    xpath('a[contains(text(), "Photos")]').click()
    sleep(2)
    ''' Download 'Photos of You' '''
    makedirs('Photos-of-You') # Make folder
    xpath('div[@class="tagWrapper"]').click() # click on first image

    main()
