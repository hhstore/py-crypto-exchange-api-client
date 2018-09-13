# import logging

from selenium import webdriver
#
# logger = logging.getLogger(__name__)
#


if __name__ == '__main__':
    options = webdriver.Chrome('/User/dev/Desktop/chromedriver')
    options.get('https://www.baidu.com')


