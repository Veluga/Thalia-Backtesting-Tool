from selenium import webdriver

import util
'''
Test navbar works properly (redirects to correct pages and displays on all pages)
as well as that all pages load sucesfully and display the navbar and social media links
'''

def test_navbar_redirect(driver, xpath, page):
    '''
    test a specific navbar link [xpath] loads page '/page/' and displays navbar
    '''
    # Navigate to navbar page
    navbar_link = driver.find_element_by_xpath(xpath)
    driver.execute_script("arguments[0].click();", navbar_link)

    # Test about page redirect and page loaded
    util.page_wait()
    if page == '/':
        assert driver.current_url == 'http://localhost:5000/'
    else:
        assert driver.current_url == ('http://localhost:5000/' + page + '/')
    # Check page has loaded properly and that navbar is displayed
    driver.find_element_by_id('navbarBasicExample')
    # Check footer with links loaded
    driver.find_element_by_class_name('footer')
    footer_text = driver.find_element_by_xpath('/html/body/footer/div/div[1]/h1')
    assert 'Or you can reach out to us on social media.' in footer_text.get_attribute('innerHTML')


def navbar_test(driver):
    driver.get('http://localhost:5000')
    driver.implicitly_wait(2) # seconds
    # Make sure we're accesing the correct webpage
    assert 'Thalia' in driver.title

    test_navbar_redirect(driver, '/html/body/nav/div[2]/div[1]/a[2]', 'about')
    test_navbar_redirect(driver, '/html/body/nav/div[2]/div[1]/div/div/a' , 'contact')
    # Test home rediret 
    test_navbar_redirect(driver, '/html/body/nav/div[2]/div[1]/a[1]', '/')
    # Test thalia logo redirect
    test_navbar_redirect(driver, '/html/body/nav/div[1]/a[1]', '/')


if __name__ == "__main__":
    driver = webdriver.Firefox()
    navbar_test(driver)
    driver.close()
    driver = webdriver.Chrome()
    navbar_test(driver)
    driver.close()

