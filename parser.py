import json
import time

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
import chromedriver_binary
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import pandas as pd



class AvitoPars:
    def __init__(self, url:str ,item:list , count=10):
        self.url = url
        self.item = item
        self.data = []
        self.count = count
        self.location = None
        self.active_product = None
        self.name_owner = None
        self.img = None
        self.span_element = None


    def __set_up(self):
        options = Options()
        # options.add_experimental_option("detach", True)
        options.add_argument('--headless')
        # options.add_argument("incognito")
        # options.add_argument('--proxy-server=50.218.57.69:80')
        # options.add_argument("user-agent=HelloWorld")
        #
        # options.headless = True
        # options.add_experimental_option("useAutomationExtension", False)
        # options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.driver = webdriver.Chrome(options=options)
        # WebDriverWait(self.driver, 10)


    def __get_url(self):
        self.driver.implicitly_wait(12)
        self.driver.get(self.url)



    def __paginator(self):
        while self.driver.find_elements(By.CSS_SELECTOR, "[data-marker='pagination-button/nextPage']") and  self.count > 0:
            self.__parse_page()
            self.driver.find_element(By.CSS_SELECTOR, "[data-marker='pagination-button/nextPage']").click()
            self.count -=1

        # next_page_buttons_selector = "[data-marker='pagination-button/nextPage']"
        # while int(self.count) > 0:
        #     next_page_buttons = self.driver.find_elements(By.CSS_SELECTOR, next_page_buttons_selector)
        #     if not next_page_buttons:
        #         break
        #     self.__parse_page()
        #     next_page_buttons[0].click()
        #     self.count-=1



    def __parse_page(self):
        self.driver.implicitly_wait(12)
        titles = self.driver.find_elements(By.CSS_SELECTOR, "[data-marker='item']")

        for title in titles:
            try:
                name = title.find_element(By.CSS_SELECTOR, "[itemprop='name']").text
            except NoSuchElementException:
                return None
            try:
                description = title.find_element(By.CSS_SELECTOR, "[class*='iva-item-descriptionStep-C0ty1']").text
            except NoSuchElementException:
                return None
            try:
                link = title.find_element(By.CSS_SELECTOR, "[data-marker='item-title']").get_attribute("href")
            except NoSuchElementException:
                return None
            try:
                price = title.find_element(By.CSS_SELECTOR, "[itemprop='price']").get_attribute("content")
            except NoSuchElementException:
                return None

            if any([item.lower() in description.lower() for item in self.item]):
                time.sleep(3)
                title.find_element(By.CSS_SELECTOR, "[data-marker='item-title']").click()

                self.driver.switch_to.window(self.driver.window_handles[1])
                info = self.driver.find_elements(By.CSS_SELECTOR, "[class='styles-module-theme-CRreZ styles-root-a5ys4']")
                for info in info:
                    try:
                        self.active_product = info.find_element(By.CSS_SELECTOR, "[class='desktop-1921dkr']").text
                    except NoSuchElementException:
                        self.active_product = None
                    try:
                        owner = info.find_elements(By.CSS_SELECTOR, "[data-marker='seller-info/name']")
                        for owner in owner:
                            self.name_owner = owner.find_element(By.CLASS_NAME, 'styles-module-size_ms-EVWML').text
                    except NoSuchElementException:
                        self.name_owner = None
                    try:
                        self.location = info.find_element(By.CSS_SELECTOR, "[class='style-item-address__string-wt61A']").text
                    except NoSuchElementException:
                        self.location = None
                    try:
                        span_elements = info.find_element(By.CLASS_NAME, 'image-frame-cover-lQG1h').get_attribute('style')
                        self.span_element = span_elements.split('url("')[1].split('")')[0].split('")')[0]
                    except NoSuchElementException:
                        self.span_element = None


                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])


            data = {
                'name': name,
                'description': description,
                'link': link,
                'price': price,
                'active_product': self.active_product,
                'name_owner': self.name_owner,
                'location': self.location,
                'img': self.span_element,


            }

            if any([item.lower() in description.lower() for item in self.item]):
                self.data.append(data)
                print(data)
                print(f"----------------{self.count}----------------")
        self.__save_data()
        # self.driver.close()

    def __save_data(self):

        df = pd.DataFrame(self.data)
        excel_file = 'avitoaddress.xlsx'

        with pd.ExcelWriter(excel_file, engine='xlsxwriter', mode='w') as writer:
            df.to_excel(writer, sheet_name='Sheet1', index=False)

        # with open("items.json", 'w', encoding='utf-8') as f:
        #     json.dump(self.data, f, ensure_ascii=False, indent=4)

    def parse(self):
        self.__set_up()
        self.__get_url()
        self.__parse_page()
        self.__paginator()
        self.__save_data()

if __name__ == "__main__":
    AvitoPars(url='https://www.avito.ru/moskva?q=%D0%BF%D0%B5%D1%80%D0%B5%D0%B2%D0%BE%D0%B7%D1%87%D0%B8%D0%BA%D0%BE%D0%B2+%D0%BF%D0%BE+%D0%BA%D0%BB%D0%B0%D1%81%D1%81%D0%B0%D0%BC+%D0%BE%D0%BF%D0%B0%D1%81%D0%BD%D0%BE%D1%81%D1%82%D0%B8+%D0%B3%D1%80%D1%83%D0%B7%D0%BE%D0%B2'
              , count=3, item=['юридический адрес', 'юрадрес']).parse()








