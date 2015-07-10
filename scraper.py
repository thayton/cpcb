#!/usr/bin/env python

import re
import string
import urlparse

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup

class CPCBScraper(object):
    def __init__(self):
        self.url = 'http://cpcb.gov.in/CAAQM/frmUserAvgReportCriteria.aspx'
        self.driver = webdriver.PhantomJS()
        self.driver.set_window_size(1120, 550)

    def scrape(self):
        self.driver.get(self.url)

        #
        # State -> City -> Station
        # 
        state_select = Select(self.driver.find_element_by_id('ddlState'))
        state_option_indexes = range(1, len(state_select.options))

        # Iterate through each state
        for state_index in state_option_indexes:
            state_select.select_by_index(state_index)

            def done_loading(driver):
                div = driver.find_element_by_id('UpdateProgress1')
                return div.is_displayed() == False            

            # Wait until city loaded
            wait = WebDriverWait(self.driver, 10)
            wait.until(done_loading)

            city_select = Select(self.driver.find_element_by_id('ddlCity'))
            city_option_indexes = range(1, len(city_select.options))            

            for city_index in city_option_indexes:
                city_select.select_by_index(city_index)

                # Wait until station loaded
                wait = WebDriverWait(self.driver, 10)
                wait.until(done_loading)


        self.driver.quit()

if __name__ == '__main__':
    scraper = CPCBScraper()
    scraper.scrape()
