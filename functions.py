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
