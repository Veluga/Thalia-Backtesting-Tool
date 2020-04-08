'''
main script for running selenium tests
'''
from selenium import webdriver

from register_test import register_test
from login_test import login_test, logout_test
from social_test import social_test
from navbar_test import navbar_test
from contact_test import contact_test
from dashboard_test import dashboard_test

# Chrome
def run_tests(driver):
    print('[0] -- Testing navbar, footer and page loading.')
    navbar_test(driver)
    print('[1] -- Testing social media integration.')
    social_test(driver)
    print('[2] -- Testing social media integration.')
    contact_test(driver)
    print('[3] -- Testing registration form.')
    register_test(driver)
    print('[4] -- Testing login form.')
    login_test(driver)
    print('[5] -- Testing dashboard.')
    dashboard_test(driver)
    print('[6] -- Testing log out')
    logout_test(driver)
    print('[-] -- Closing driver.')
    driver.close()


print('Testing on Mozilla Firefox webdriver ...')
run_tests(webdriver.Firefox())
print('Testing on Google Chrome webdriver ...')
run_tests(webdriver.Chrome())
print('Testing successfull')