import requests as requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.wait import WebDriverWait


class TestSomeThing:

    def test_get_200(self):
        response = requests.get("https://habr.com/ru/all")

        print(response.status_code)
        PATH = "Users/den/Desktop/api_tests/geckodriver"
        with webdriver.Firefox(PATH) as driver:

            wait = WebDriverWait(driver, 10)
            driver.get("https://habr.com/ru/all/")
            list_of_all_links = driver.find_elements_by_name("href").sort(str.startswith("https://"))
            print(list_of_all_links)
            # first_result = wait.until(presence_of_element_located((By.CSS_SELECTOR, "h3")))
            # print(first_result.get_attribute("textContent"))

