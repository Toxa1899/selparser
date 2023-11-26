import json
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_binary
import pandas as pd


class AvitoPars:
    def __init__(self, url: str,item: list ,count = 10):
        self.url = url
        self.item = item
        self.count = count
        self.data = []


    def __set_up(self):
        self.driver = webdriver.Chrome()


    def __get_url(self):
        self.driver.get(self.url)

    def __paginator(self):
        while self.driver.find_elements(By.CSS_SELECTOR, "[data-marker='pagination-button/nextPage']") and self.count > 1:
            self.__parser()
            self.driver.find_element(By.CSS_SELECTOR, "[data-marker='pagination-button/nextPage']").click()
            self.count -= 1


    def __parser(self):
        self.driver.implicitly_wait(12)
        title_avito = self.driver.find_elements(By.CSS_SELECTOR, "[data-marker='item']")
        for title in title_avito:
            name = title.find_element(By.CSS_SELECTOR, "[data-marker='item-title']").text

            account = title.find_elements(By.CSS_SELECTOR, "[data-marker='item-title']")
            for account in account:
                time.sleep(5)
                account.click()
                self.driver.switch_to.window(self.driver.window_handles[1])
                account_user_name = self.driver.find_element(By.CSS_SELECTOR, "[data-marker='seller-info/name']").text

                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])



                data = {
                    'name': name,
                    'User_name': account_user_name,
                }

                if any([item.lower() in name.lower() for item in self.item]):
                    self.data.append(data)

            self.save_date()



    def save_date(self):

        with open('avito.json', 'w', encoding='utf-8')as f:
            json.dump(self.data, f , ensure_ascii=False, indent= 6)






    def pars(self):
        self.__set_up()
        self.__get_url()
        self.__paginator()
        self.__parser()
        self.save_date()

if __name__ == "__main__":
    AvitoPars(url='https://www.avito.ru/moskva/uslugi?cd=1&q=%D1%8E%D1%80%D0%B8%D0%B4%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B9+%D0%B0%D0%B4%D1%80%D0%B5%D1%81', item=['юридический адрес', 'юрадрес'], count=4).pars()
