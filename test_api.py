import enum
from datetime import datetime
from enum import Enum
from time import sleep

import allure
import pytest
import requests as requests
from allure_commons.types import AttachmentType
from selenium import webdriver
from pathlib import Path

# путь до локального драйвера Firefox в проекте

path_to_geckodriver = Path("geckodriver").resolve()
execute_firefox = webdriver.Firefox(executable_path=path_to_geckodriver)

main_url = "https://mail.ru"  # основная ссылка для теста


# Allure классификация
@enum.unique
class Feature(Enum):
    CLICK_ELEMENT = 'Нажатие на элемент'
    CHECK_EXIST_ELEMENT = 'Проверка наличия элемента'
    FUNC_TEST = 'Функциональное тестирование'


# Allure классификация
@enum.unique
class Level(Enum):
    """
    По убыванию - в зависимости от важности
    """
    BLOCKER = 'blocker'
    CRITICAL = 'critical'
    NORMAL = 'normal'
    MINER = 'miner'
    TRIVIAL = 'trivial'


class TestSomeThing:

    @allure.feature(Feature.CHECK_EXIST_ELEMENT.value)
    @allure.story('Проверка на работоспособность сайта,'
                  'в случае удачи поиск всех доступных ссылок,'
                  'вывод в файлы отчета об ответе')
    @allure.severity(severity_level=Level.CRITICAL.value)
    def test_get_all_href_respond(self):

        # очистка файлов отчета для новой записи

        clear_issue_report = open('response_issues.txt', 'w')
        clear_issue_report.write("Test started at " + str(datetime.today()) + "\n" + "\n")
        clear_issue_report.close()

        clear_positive_report = open('response_200.txt', 'w')
        clear_positive_report.write("Test started at " + str(datetime.today()) + "\n" + "\n")
        clear_positive_report.close()

        response = requests.get(main_url)
        answer = response.status_code

        # Проверка доступности основной ссылки

        if 200 <= answer < 300:
            with execute_firefox as driver:  # запуск драйвера на полный экран

                driver.maximize_window()
                driver.get(main_url)

                # скриншот открытой страницы для Allure отчета

                allure.attach(driver.get_screenshot_as_png(), name="output result",
                              attachment_type=AttachmentType.PNG)
                links = driver.find_elements_by_tag_name("a")

                # получение списка элементов содержащих ссылки

                for lnk in links:

                    # get_attribute() получение всех атрибутов ссылок в дереве элементов

                    testing_link = lnk.get_attribute('href')

                    # условие что ссылка не пустая строка

                    if testing_link is not None:

                        if testing_link.startswith("/"):
                            testing_link = main_url + testing_link
                            # отправка запроса в полученную с сайта ссылку

                            response = requests.get(testing_link)
                            answer = response.status_code
                        else:
                            pass

                        if answer == 200:  # условие ответа равного 200

                            # запись информации в файл

                            positive_report_file = open("response_200.txt", "a+")
                            positive_report_file.write("\n" + " link status is " + str(answer) +
                                                       " " + str(datetime.now()) + "\n" + testing_link + "\n")
                            positive_report_file.close()

                        elif answer != 200:  # условие ответа не равного 200

                            # запись информации в файл

                            issue_report_file = open("response_issues.txt", "a+")
                            issue_report_file.write("\n" + " link status is " + str(answer) +
                                                    " " + str(datetime.now()) + "\n" + testing_link + "\n")
                            issue_report_file.close()

                        else:
                            continue
        else:
            pytest.fail('Site is dead. Link is broken')

    @allure.feature(Feature.FUNC_TEST.value)
    @allure.story('Переход по всем ссылкам сайта и сверка адреса с ссылкой оригинала')
    @allure.severity(severity_level=Level.CRITICAL.value)
    def test_all_href_correction_transition(self):

        # инициализация драйвера

        with execute_firefox as driver:

            driver.maximize_window()
            driver.implicitly_wait(5)

            # открытие искомой страницы

            driver.get(main_url)
            allure.attach(driver.get_screenshot_as_png(), name="output result",
                          attachment_type=AttachmentType.PNG)

            # скриншот искомой страницы

            links = driver.find_elements_by_tag_name("a")
            for lnk in links:
                testing_link = lnk.get_attribute('href')

                if testing_link is not None:  # условие что ссылка не пустая строка

                    if testing_link.startswith("/"):
                        # условие если ссылка не полная
                        testing_link = main_url + testing_link

                    another_driver = execute_firefox
                    another_driver.execute_script("window.open('');")  # открытие дополнительного окна браузера
                    another_driver.switch_to.window(driver.window_handles[1])  # переход в окно браузера
                    another_driver.get(testing_link)  # открытие ссылки
                    sleep(3)
                    assert testing_link == another_driver.current_url  # проверка на соответствие текущей ссылке
                    another_driver.switch_to.window(driver.window_handles[0])  # возврат к основному окну
