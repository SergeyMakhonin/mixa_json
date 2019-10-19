from selenium import webdriver

from OptaWebTools import opta_login
from logging_and_configuration import json_reader

config = json_reader('../config.json')

driver = webdriver.Firefox()
driver.get(config['opta_reaper']['opta_host'])

opta_login(driver, config)

driver.close()

