from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from logging_and_configuration import log


def wretched_wait(driver, config, id):
    try:
        timeout = config['opta_reaper']['timeout']
        element_present = EC.presence_of_element_located((By.ID, id))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print("Timed out waiting for {id}".format(id=id))


def opta_login(driver, config):
    try:
        # wait for username field
        username_id = 'lm3-email-lm3_0'
        wretched_wait(driver, config, username_id)

        # put login
        user_field = driver.find_element_by_id(username_id)
        user_field.clear()
        user_field.send_keys('epl@rambler-co.ru')
    except NoSuchElementException as e:
        log('Unable to find element: {e}'.format(e=e))

    try:
        # wait for password field
        password_id = 'lm3-password-lm3_0'
        wretched_wait(driver, config, password_id)

        # put password
        pass_field = driver.find_element_by_id(password_id)
        pass_field.send_keys('10WVe305X')
        pass_field.send_keys(Keys.RETURN)
    except NoSuchElementException as e:
        log('Unable to find element: {e}'.format(e=e))