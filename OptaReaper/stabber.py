from selenium import webdriver

from OptaReaper.opta_web_tools import opta_login, opta_select_match
from logging_and_configuration import json_reader

config = json_reader('../config.json')

driver = webdriver.Firefox()
driver.get(config['opta_reaper']['opta_host'])

opta_login(driver, config)
opta_select_match(driver, config)

driver.close()
