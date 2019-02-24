import re
import imageio
import time
from datetime import datetime
from selenium import webdriver

# Open browser
driver = webdriver.Chrome('../chromedriver')
driver.get('https://wwww.facebook.com/login')
SLEEP_INTERVAL = 0.1


class Facebook(object):

    def rename_img(self, i, folder):
        date = self.async_attribute('span[@id="fbPhotoSnowliftTimestamp"]/a/abbr', 'title')
        # Shorten string
        if ' at ' in date:
            date = date[:date.find(' at ')]

        num_commas = len(re.compile(',').findall(date))
        if  num_commas == 2:
            date = date[date.find(',')+2:]
        elif num_commas == 0:
            date = date[:date.find(' ')] + ' 01,' + date[date.find(' '):]

        # Add 0 to the date string if it's a single-digit # day
        date_10_digit = date.find(', 20') - 2
        if date_10_digit == ' ':
            date = date[:day_10_digit+1] + '0' + date[day_10_digit+1:]
        # long string => datetime => short string
        file_date = datetime.strftime(datetime.strptime(date, '%B %d, %Y'), '%Y-%m-%d')
        # Add image numbering convention from 0001 to 9999
        file_num = '0' * (4-len(str(i))) + str(i)
        filename = folder + file_date + '-' + file_num + '.jpg'
        return filename


    def xpath(self, path, collection=False):
        if not collection:
            return driver.find_element_by_xpath('//' + path)
        else:
            return driver.find_elements_by_xpath('//' + path)


    def async_attribute(self, path, attribute):
        time.sleep(SLEEP_INTERVAL)
        try:
            value = self.xpath(path).get_attribute(attribute)
            if value is not None:
                return value
        except:
            return self.async_attribute(path, attribute)


    def async_send_keys(self, path, keys):
        time.sleep(SLEEP_INTERVAL)
        try:
            self.xpath(path).send_keys(keys)
            return
        except:
            return self.async_send_keys(path, keys)


    def async_click(self, path):
        time.sleep(SLEEP_INTERVAL)
        try:
            self.xpath(path).click()
            return
        except:
            return self.async_click(path)


    def run(self, folder):
        i = 0
        first_img = None
        time.sleep(1)
        while True:
            img_link = self.async_attribute('img[@class="spotlight"]', 'src')
            if first_img is None:
                first_img = img_link
            # Make sure that we're not re-downloading the first image in the album
            elif img_link == first_img:
                break

            # Continue with main loop
            i +=1
            filename = self.rename_img(i, folder)
            img = imageio.imread(img_link)
            imageio.imwrite(filename, img)
            # Go to next image
            self.async_click('a[@title="Next"]')
