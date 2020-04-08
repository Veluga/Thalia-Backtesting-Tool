from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from register_test import register_test
from login_test import login_test, logout_test
from navbar_test import test_navbar_redirect

import util

"""
Test backtesting dashboard
"""

def tab_selected_test(driver, selected_tab, tabs):
    '''
    check only specific tab selected
    '''
    for tab in tabs:
        if tab == selected_tab:
            assert 'tab--selected' in driver.find_element_by_id(tab).get_attribute('class')
        else:
            assert 'tab--selected' not in driver.find_element_by_id(tab).get_attribute('class')


def dashboard_test(driver):
    tabs = ["tickers","summary","metrics","returns", "drawdowns", "assets"]
    driver.get("http://localhost:5000")
    driver.implicitly_wait(2)  # seconds

    # Make sure we're accesing the correct webpage
    assert "Thalia" in driver.title

    # Navigate to dashboard and check navbar
    navbar_link = driver.find_element_by_xpath('/html/body/nav/div[2]/div[1]/a[3]')
    driver.execute_script("arguments[0].click();", navbar_link)

    assert driver.current_url == "http://localhost:5000/dashboard/"
    driver.find_element_by_id("navbarBasicExample")


    # Check selection tab
    tab_selected_test(driver, 'tickers', tabs)

    input_money = driver.find_element_by_id("input-money")
    util.input_clear(input_money)
    input_money.send_keys(util.init_balance)
    
    portfolio_name = driver.find_element_by_id("portfolio-name-1")
    util.input_clear(portfolio_name)
    portfolio_name.send_keys(util.p_name)

    input_contribution = driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div/div[2]/div[2]/div[2]/div[1]/div/div[3]/div/input')
    input_contribution.clear()
    input_contribution.send_keys(util.cont_amount)

    contr_freq = driver.find_element_by_xpath("//input[@id='contribution-dropdown-1']")
    contr_freq.send_keys('Monthly')
    contr_freq.send_keys(Keys.RETURN)

    reb_freq = driver.find_element_by_xpath("//input[@id='rebalancing-dropdown-1']")
    reb_freq.send_keys('Monthly')
    contr_freq.send_keys(Keys.RETURN)

    lazy_ports = driver.find_element_by_xpath("//input[@id='lazy-portfolios-1']")    
    lazy_ports.send_keys('Growth Portfolio')
    lazy_ports.send_keys(Keys.RETURN)

    # Check adding portfolios
    for i in range(1,5):
        for j in range(1,5):
            if(j <= i):
                assert 'block' == driver.find_element_by_id("portfolio-" + str(j)).value_of_css_property("display")
            else:
                assert 'none' == driver.find_element_by_id("portfolio-" + str(j)).value_of_css_property("display")

        add_port = driver.find_element_by_id("add-portfolio-btn")
        add_port.click()
    
    submit = driver.find_element_by_id("submit-btn")
    submit.click()


    # Test tab selection
    for tab in tabs:
        tab_select = driver.find_element_by_id(tab)
        tab_select.click()
        tab_selected_test(driver, tab, tabs)
        

    





    
    


if __name__ == "__main__":
    '''
    driver = webdriver.Firefox()
    register_test(driver)
    login_test(driver)
    dashboard_test(driver)
    driver.close()
    '''
    driver = webdriver.Chrome()
    #register_test(driver)
    login_test(driver)
    dashboard_test(driver)
    #logout_test(driver)
    #driver.close()
