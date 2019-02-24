## Download your photos on Facebook to your local computer.
### By: Carter Carlson

### Description
This program uses Selenium to download your Facebook images to your local computer.  The images are saved
within named folders to match the structure of how Facebook stores your images.  Facebook has
3 primary image folders:

1. Photos Of You
2. Your Photos
3. Albums
    * Videos (auto-generated)
    * Featured Photos (auto-generated)
    * Profile Pictures
    * album 1
    * album 2
    * album 3...

This version does not download `Videos` or `Featured Photos`.

### Instructions
1. Add your username/password to the correct boxes in __api.csv__.
2. [Install Python](https://www.python.org/downloads/)
3. Clone this repository
    `git clone https://github.com/cartercarlson/fb-images`
4. Command into repository
    `cd fb-images`
5. Install requirements
    `pip install -m requirements.txt`
6. Start the downloader
    `python main.py`
7. After the bot logs you in, exit out of the Facebook popup asking about notifications.
8. Once the script is done, your images will be organized within the `Photos` folder.
