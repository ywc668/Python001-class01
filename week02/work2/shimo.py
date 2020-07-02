import time
from getpass import getpass

from selenium import webdriver

try:
    browser = webdriver.Chrome()
    # 需要安装chrome driver, 和浏览器版本保持一致
    # http://chromedriver.storage.googleapis.com/index.html

    browser.get('https://shimo.im/login?from=home')
    time.sleep(1)

    mobile_or_email = input('mobile or email to login: ')
    password = getpass('password: ')

    browser.find_element_by_xpath('//input[@type="text"]').send_keys(mobile_or_email)
    browser.find_element_by_xpath('//input[@type="password"]').send_keys(password)
    time.sleep(3)

    browser.find_element_by_xpath('//button[@class="sm-button submit sc-1n784rm-0 bcuuIb"]').click()
    time.sleep(5)

except Exception as e:
    print(e)
else:
    browser.close()
