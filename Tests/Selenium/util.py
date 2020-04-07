'''
Utilities for UI selenium tests
'''
from time import sleep

# credentials for testing
uname = 'selenium_test0'
pwd = 'selenium_test_pwd0'

# correct url's for Thalia social media
fb_url = 'https://www.facebook.com/Thalia-Backtester-101459001526511/'
twitter_url = 'https://twitter.com/Thalia99627941'

# test message for contact form
email = 'selenium_test_email0'
title = 'selenium_test_title0'
contents = 'selenium_test_contents0'

def page_wait():
    '''
    wait for page to fully load.(Built in implicit wait does not work
    when checking redirects to specific addresses as there is no element
    missing but rather an incorrect value)
    '''
    sleep(2)
