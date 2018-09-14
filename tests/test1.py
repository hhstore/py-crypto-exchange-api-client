# import logging
import time
from pprint import pprint

from selenium import webdriver
#
# logger = logging.getLogger(__name__)


if __name__ == '__main__':

    options = webdriver.Chrome()
    try:
        pprint("********************")
        options.get('https://www.okex.com/account/login')
        pprint("======================")
    except Exception as e:
        pprint(e)
        pass

    time.sleep(1)
    pprint(1)
    while True:
        try:
            # pprint(options.current_url)
            pprint("**************")
            time.sleep(1)
            try:
                options.find_element_by_class_name('dialog-confirm-btn').click()
            except Exception as e:
                pass
            pprint('点击')
            username = options.find_element_by_name('username')
            password = options.find_element_by_name('password')
            username.send_keys('m_mone@163.com')
            pprint('输入用户名')
            password.send_keys('Mtf.110/')
            pprint('输入密码')
            options.find_element_by_class_name('login-btn').click()
            break
        except Exception as e:
            # pprint(e)
            continue

    time.sleep(5)
    pprint(2)
    while True:
        try:
            # pprint(options.current_url())
            options.find_element_by_class_name('send-code-btn').click()
            code = input('请输入手机验证码')
            options.find_element_by_class_name('send-code').send_keys(code)
            options.find_element_by_class_name('confirm-btn').click()
            break
        except Exception as e:
            continue
    time.sleep(3)
    pprint(3)
    while True:
        # pprint(options.current_url())
        pprint('获取token值')
        token = options.execute_script("return window.localStorage.getItem('token');")
        pprint(token)
        if token:
            break
    options.close()
