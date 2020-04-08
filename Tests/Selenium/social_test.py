from selenium import webdriver

import util
'''
Tests for social media links and integrations
'''

def social_test(driver):
    driver.get("http://localhost:5000")
    driver.implicitly_wait(2) # seconds
    
    # Make sure we're accesing the correct webpage
    assert 'Thalia' in driver.title

    fb_link = driver.find_element_by_class_name('fa-facebook')
    fb_link.click()
    
    # Test redirect
    util.page_wait()
    assert util.fb_url == driver.current_url

    driver.get("http://localhost:5000")
    twitter_link = driver.find_element_by_class_name('fa-twitter')
    twitter_link.click()

    # Test redirect
    util.page_wait()
    assert util.twitter_url == driver.current_url




if __name__ == "__main__":
    driver = webdriver.Firefox()
    social_test(driver)
    driver.close()

    driver = webdriver.Chrome()
    social_test(driver)
    driver.close()

