from os import makedirs, remove
from shutil import move
from time import sleep
import numpy as np
import pandas as pd
from functions import *


# Log in to Facebook
login, password = pd.read_csv('login.csv').values[0]
xpath('input[@id="email"]').send_keys(login)
xpath('input[@id="pass"]').send_keys(password)
xpath('button[@id="loginbutton"]').click()

# Click on profile
t_0 = 0
wait_for_closed_notification(t_0)

# Go to photos
sleep(1)
xpath('a[contains(text(), "Photos")]').click()

''' Download 'Photos of You' '''
placeholder = 'Photos-of-You/2000-01-01-001.jpg'

makedirs('Photos-of-You') # Make folder
open(placeholder, 'a').close() # Make placeholder img
xpath('div[@class="tagWrapper"]').click() # click on first image
sleep(1)
img_count = 1

main(img_count)
