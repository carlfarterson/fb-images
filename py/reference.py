facebook = 'https://www.facebook.com/'
url = driver.current_url
username = url[url.find('.com/') + 5:]

def Photos_of_You():
    driver.get(facebook + username + '/photos_of')
    return


def Your_Photos():
    driver.get(facebook + username + '/photos_all')
    return

def Albums():
    driver.get(facebook + username + '/photos_albums')
    return
