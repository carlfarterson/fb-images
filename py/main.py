import time
from os import makedirs
import pandas as pd
from facebook import driver, Facebook

fb = Facebook()
SLEEP_INTERVAL = 0.1

makedirs('../Photos')
makedirs('../Photos/Photos of You')
makedirs('../Photos/Your Photos')
makedirs('../Photos/Albums')

# Log in
login, password = pd.read_csv('../login.csv').values[0]
fb.async_send_keys('input[@id="email"]', login)
fb.async_send_keys('input[@id="pass"]', password)
fb.async_click('button[@id="loginbutton"]')


# Click on profile and get username
fb.async_click('a[@title="Profile"]/span')
url = driver.current_url
username = url[url.find('.com/') + 5:]


''' Photos of You '''
driver.get('https://www.facebook.com/' + username + '/photos_of')
fb.async_click('div[@class="tagWrapper"]')
fb.run('../Photos/Photos of You/')


''' Your Photos '''
driver.get('https://www.facebook.com/' + username + '/photos_all')
fb.async_click('div[@class="tagWrapper"]')
fb.run('../Photos/Your Photos/')


''' Albums '''
driver.get('https://www.facebook.com/' + username + '/photos_albums')
albums = fb.xpath('div[@id="pagelet_timeline_medley_photos"]/div/div/div/table/tbody/tr/td/div/a', True)[1:]

dup_count = 1
links = []
for album in albums:
    links.append(album.get_attribute('href'))

for link in links:
    driver.get(link)
    time.sleep(2)
    title = fb.xpath('h1[@class="fbPhotoAlbumTitle"]').text.strip()
    if title != "Videos" and title != "Featured Photos":
        fb.xpath('div[@id="fbTimelinePhotosContent"]/div[1]/div[2]').click()
        folder = '../Photos/Albums/' + title
        try:
            makedirs(folder)
        except:
            folder += ('_' + str(dup_count))
            makedirs(folder)
            dup_count += 1


        fb.run(folder + '/')

driver.close()
