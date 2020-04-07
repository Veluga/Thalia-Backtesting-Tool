from selenium import webdriver

import util

"""
Test social media links
"""


def social_test(driver):
    driver.get("http://localhost:5000")
    driver.implicitly_wait(2)  # seconds

    # Make sure we're accesing the correct webpage
    assert "Thalia" in driver.title

    fb_link = driver.find_element_by_xpath("/html/body/footer/div/div[2]/a[2]")
    driver.execute_script("arguments[0].click();", fb_link)

    # Test redirect
    util.page_wait()
    assert util.fb_url == driver.current_url

    driver.get("http://localhost:5000")
    twitter_link = driver.find_element_by_xpath("/html/body/footer/div/div[2]/a[1]")
    driver.execute_script("arguments[0].click();", twitter_link)

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
