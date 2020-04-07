from selenium import webdriver

import util

"""
Test logging in as default user 'asdf' on Thalia websie
"""


def login_test(driver):
    driver.get("http://localhost:5000")
    driver.implicitly_wait(2)  # seconds
    # Make sure we're accesing the correct webpage
    assert "Thalia" in driver.title

    # Navigate to log in form
    login_button = driver.find_element_by_xpath(
        "/html/body/nav/div[2]/div[2]/div/div/a[2]"
    )
    driver.execute_script("arguments[0].click();", login_button)

    # Test redirect
    util.page_wait()
    assert "http://localhost:5000/login/" == driver.current_url

    # Fill in login form
    uname_field = driver.find_element_by_xpath(
        "/html/body/div/section/div/div/div/div[2]/form/div/div[1]/input"
    )
    uname_field.send_keys(util.uname)
    pwd_field = driver.find_element_by_xpath(
        "/html/body/div/section/div/div/div/div[2]/form/div/div[2]/input"
    )
    pwd_field.send_keys(util.pwd)

    submit = driver.find_element_by_xpath(
        "/html/body/div/section/div/div/div/div[2]/form/div/div[4]/div/button"
    )
    driver.execute_script("arguments[0].click();", submit)

    # Check log in sucessfull
    util.page_wait()
    disabled_login_buttons = driver.find_element_by_xpath(
        "/html/body/nav/div[2]/div[2]/div/div"
    )

    assert "http://localhost:5000/" == driver.current_url
    assert ("Hi " + util.uname + "!") in disabled_login_buttons.get_attribute(
        "innerHTML"
    )


if __name__ == "__main__":
    from register_test import register_test

    driver = webdriver.Firefox()
    register_test(driver)
    login_test(driver)
    driver.close()

    driver = webdriver.Chrome()
    register_test(driver)
    login_test(driver)
    driver.close()
