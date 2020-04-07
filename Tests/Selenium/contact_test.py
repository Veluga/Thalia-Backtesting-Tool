from selenium import webdriver
import pandas as pd
import numpy as np

import util
'''
Test social media links
'''

def contact_test(driver):
    driver.get("http://localhost:5000")
    driver.implicitly_wait(2) # seconds
    
    # Make sure we're accesing the correct webpage
    assert 'Thalia' in driver.title

    contact = driver.find_element_by_xpath('/html/body/nav/div[2]/div[1]/div/div/a')
    driver.execute_script("arguments[0].click();", contact)

    # Fill in contact form
    util.page_wait()

    email_field = driver.find_element_by_xpath('/html/body/div/section/div/div/div/div[5]/form/div/div[2]/input')
    email_field.send_keys(util.email)

    title_field = driver.find_element_by_xpath('/html/body/div/section/div/div/div/div[5]/form/div/div[3]/input')
    title_field.send_keys(util.title)

    contents_field = driver.find_element_by_xpath('/html/body/div/section/div/div/div/div[5]/form/div/div[4]/textarea')
    contents_field.send_keys(util.contents)

    send_feedback_btn = driver.find_element_by_xpath('/html/body/div/section/div/div/div/div[5]/form/div/div[5]/div/button')   
    driver.execute_script("arguments[0].click();", send_feedback_btn)

    # Check message was recorded
    df0 = pd.read_csv('../../feedback.csv')
    submitted = np.array([util.email,util.title,util.contents])
    assert (df0 == submitted).all(1).any()

if __name__ == "__main__":
    driver = webdriver.Firefox()
    contact_test(driver)
    driver.close()
    driver = webdriver.Chrome()
    contact_test(driver)
    driver.close()

