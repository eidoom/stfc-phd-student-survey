#!/usr/bin/env python
# coding=utf-8

from configparser import ConfigParser
from datetime import datetime

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class Data:
    def __init__(self, settings_file="config.cfg"):
        config = ConfigParser()
        config.read(settings_file)

        for section in ("web_page", "details"):
            for key, value in config[section].items():
                setattr(self, key, value)

        for key, value in config["details_capitalise"].items():
            setattr(self, key, value.title())


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

    def click_circle_nested(self, field):
        field_name = " ".join(field.split("_"))
        try:
            selection = self.driver.find_element_by_xpath(
                f"//strong[contains(text(),'{field_name}')]/../../../div/div/label[contains(text(), '{getattr(self.data, field)}')]/../input")
        except NoSuchElementException:
            selection = self.driver.find_element_by_xpath(
                f"//strong[contains(text(),'{field_name}')]/../../div/div/label[contains(text(), '{getattr(self.data, field)}')]/../input")
        selection.click()

    def click_circle(self, field):
        selection = self.driver.find_element_by_xpath(
            f"//label[contains(text(), '{getattr(self.data, field)}')]/../input")
        selection.click()

    def row_choice(self, *fields):
        for field in fields:
            value = 1 if eval(getattr(self.data, field)) else 3
            selection = self.driver.find_element_by_xpath(
                f"//th[contains(text(),'{field}')]/../td/input[@value='{value}']")
            selection.click()


def main():
    data = Data()
    print(data.site + str(datetime.now().year))
    exit()
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

    scraper.click_circle("studentship_type")

    scraper.next_page()

    scraper.click_circle("research_field")
    scraper.click_circle("funding_form")
    scraper.click_circle("year")
    scraper.click_circle("time_basis")
    scraper.click_circle("discussed_funding_period")
    scraper.drop_down_input("funded_period")

    scraper.next_page()

    if data.year == "First":
        scraper.row_choice("subject", "pursue", "enhance", "plans", "alternative")
        scraper.click_circle("rate_induction")
        scraper.next_page()

    scraper.click_circle_nested("how_often_do_you_discuss_your_research_with_your_supervisor")
    scraper.click_circle("receive_help/advice_from_a_second_supervisor_or_other_people")

    supervision_useful = driver.find_element_by_xpath(f"//input[@value='{data.supervision_useful}']")
    supervision_useful.click()

    scraper.click_circle_nested("opportunity_to_attend_group_/_departmental_seminars")
    scraper.click_circle_nested("any_problems_or_difficulties_with_your_supervisory_team")
    scraper.click_circle_nested("any_problems_or_difficulties_with_other_members_of_your_department")

    scraper.next_page()

    input("Press any key when done ")
    driver.close()


if __name__ == "__main__":
    main()
