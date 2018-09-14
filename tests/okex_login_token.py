# import logging
import time
from pprint import pprint

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#
# logger = logging.getLogger(__name__)


def okex_login():
    # 设置无头
    options = Options()
    options.add_argument("--headless")  # Runs Chrome in headless mode.
    options.add_argument('--no-sandbox')  # Bypass OS security model
    options.add_argument('start-maximized')  #
    options.add_argument('disable-infobars')
    options.add_argument("--disable-extensions")
    driver = webdriver.Chrome(chrome_options=options,)

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

    username = input('请输入用户名:\n')
    password = input('请输入密码:\n')

    driver.find_element_by_name('username').send_keys(username)
    driver.find_element_by_name('password').send_keys(password)
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
