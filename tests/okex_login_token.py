# import logging
import time
from pprint import pprint

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#
# logger = logging.getLogger(__name__)


def okex_login():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)

    pprint("********************")
    driver.get('https://www.okex.com/account/login')
    pprint("======================")

    try:
        driver.find_element_by_class_name('dialog-confirm-btn').click()
    except Exception as e:
        print(e)
        pass

    WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located
    )

    username = driver.find_element_by_name('username')
    password = driver.find_element_by_name('password')

    username.send_keys('m_mone@163.com')
    password.send_keys('Mtf.110/')
    driver.find_element_by_class_name('login-btn').click()

    # pprint(options.current_url())
    driver.find_element_by_class_name('send-code-btn').click()

    code = input('请输入手机验证码:\n')
    driver.find_element_by_class_name('send-code').send_keys(code)
    driver.find_element_by_class_name('confirm-btn').click()

    time.sleep(1)
    # pprint(options.current_url())
    token = driver.execute_script("return window.localStorage.getItem('token');")
    pprint(token)

    driver.quit()


if __name__ == '__main__':
    okex_login()
