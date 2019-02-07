#!/usr/bin/env python
# coding=utf-8

from configparser import ConfigParser

from selenium import webdriver


# from selenium.webdriver.common.keys import Keys

class Data:
    def __init__(self, settings_file="config.cfg"):
        config = ConfigParser()
        config.read(settings_file)

        webpage = config["webpage"]
        self.site = webpage["site"]
        self.title = webpage["title"]

        details = config["details"]
        self.forename = details["forename"].title()
        self.surname = details["surname"].title()
        self.email = details["email"]
        self.gender = details["gender"].title()
        self.university = details["university"].title()
        self.department = details["department"].title()
        self.studentship_type = details["studentship_type"]


class Scraper:
    def __init__(self, driver, data):
        self.driver = driver
        self.data = data

    def text_input(self, field):
        selection = self.driver.find_element_by_xpath(f"//th[contains(text(),'{field.capitalize()}')]/../td/input")
        selection.send_keys(getattr(self.data, field))

    def drop_down_input(self, field):
        selection = self.driver.find_element_by_xpath(f"//option[contains(text(),'{getattr(self.data, field)}')]")
        selection.click()

    def next_page(self):
        next_button = self.driver.find_element_by_xpath("//button[@class='btn btn-next']")
        next_button.click()


def main():
    data = Data()
    driver = webdriver.Chrome()
    driver.get(data.site)
    assert data.title == driver.title

    scraper = Scraper(driver, data)

    scraper.next_page()

    scraper.text_input("forename")
    scraper.text_input("surname")

    email = driver.find_element_by_xpath("//th[contains(text(), 'Email address')]/../td/input")
    email.send_keys(data.email)

    scraper.drop_down_input("gender")
    scraper.drop_down_input("university")

    department = driver.find_element_by_xpath(
        f"//div[contains(text(), '{data.university}')]/../div/div/label[contains(text(), '{data.department}')]/../input")
    department.click()

    studentship_type = driver.find_element_by_xpath(
        f"//label[contains(text(), '{data.studentship_type}')]/../input")
    studentship_type.click()

    scraper.next_page()

    input("Press any key when done ")
    driver.close()


if __name__ == "__main__":
    main()
