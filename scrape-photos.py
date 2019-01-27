from os import makedirs, remove
from shutil import move
from time import sleep
import numpy as np
import pandas as pd
from functions import *

login, password = pd.read_csv('login.csv').values[0]

def main(img_count):
    xpath('span[contains(text(), "Options")]').click() # Click on options
    sleep(1)
    download_image() # download image
    sleep(1)

    if img_count == 1:
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

    move(most_recent_file('~/Downloads'), filename)
    xpath('a[@title="Next"]').click() # Go to next image
    sleep(1)
    return main(img_count + 1)


if __name__ == '__main__':
    # Log in to Facebook
    xpath('input[@id="email"]').send_keys(login)
    xpath('input[@id="pass"]').send_keys(password)
    xpath('button[@id="loginbutton"]').click()

    # Click on profile
    t_0 = 0
    wait_for_closed_notification(t_0)
    # Go to photos
    sleep(3)
    xpath('a[contains(text(), "Photos")]').click()
    sleep(5)
    ''' Download 'Photos of You' '''
    makedirs('Photos-of-You') # Make folder
    xpath('div[@class="tagWrapper"]').click() # click on first image
    sleep(1)
    main(1)
