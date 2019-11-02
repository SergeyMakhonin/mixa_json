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


def opta_select_match(driver, config, competition, date, match):
    # competition select
    competition_select_dropbox_id = 'competition-select-lm3_0'

    # wait for dropbox and find it
    wretched_wait(driver, config, competition_select_dropbox_id)
    competition_select_dropbox = driver.find_element_by_id(competition_select_dropbox_id)

    # get its options and find desired ones to reap
    competition_options = competition_select_dropbox.find_elements_by_tag_name('option')
    for competition_option in competition_options:
        if competition_option.get_attribute('text') in config['opta_reaper']['competition_to_reap']:
            competition_option.click()
            log('Competiton chosen: {c}'.format(c=config['opta_reaper']['competitions_to_reap']))

        # wait for matches date input
        matches_date_input_id = 'datepicker'
        wretched_wait(driver, config, matches_date_input_id)
        matches_date_picker = driver.find_element_by_id(matches_date_input_id)
        for date in config['opta_reaper']['matche_dates']:
            matches_date_picker.clear()
            matches_date_picker.send_keys(date)
            matches_date_picker.send_keys(Keys.RETURN)
            log('Chosen date: {date}'.format(date=date))
