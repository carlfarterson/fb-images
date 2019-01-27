from os import makedirs, remove
from shutil import move
from time import sleep
import numpy as np
import pandas as pd
from functions import *

def main(img_count, first_img=None):

    xpath('span[contains(text(), "Options")]').click() # Click on options
    sleep(1)
    download_image() # download image
    if first_img is None:
        # Get the name of the first file downloaded to ensure we're not downloading
        # another file w/ the same name.
        file = most_recent_file('~/Downloads')
        first_img = file[file.find('Downloads/')+10:file.find('.jpg')]
    elif first_img in most_recent_file('~/Downloads'):
        remove(most_recent_file('~/Downloads'))
        print('Download complete.')
        driver.close()
        return

    # continue with main loop
    filename = rename_img(img_count)
    sleep(1)
    move(most_recent_file('~/Downloads'), filename)
    xpath('a[@title="Next"]').click() # Go to next image
    sleep(1)
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
    wait_for_closed_notification(t_0)
    # Go to photos
    sleep(2)
    xpath('a[contains(text(), "Photos")]').click()
    sleep(2)
    ''' Download 'Photos of You' '''
    makedirs('Photos-of-You') # Make folder
    xpath('div[@class="tagWrapper"]').click() # click on first image
    sleep(2)
    main(1)
