import json
import time

from bs4 import BeautifulSoup
from selenium.common import NoSuchElementException, StaleElementReferenceException, ElementNotInteractableException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
import chromedriver_binary
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import pandas as pd
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class AvitoPars:
    def __init__(self, url:str ,item:list , count=10):
        self.url = url
        self.item = item
        self.data_list = []
        self.count = count


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
        self.driver = webdriver.Chrome()
        # WebDriverWait(self.driver, 10)


    def __get_url(self):


        self.driver.maximize_window()
        self.driver.get(self.url)

        login_input = self.driver.find_element(By.ID, 'login')
        login_input.clear()
        login_input.send_keys('ralz9-ralz9@mail.ru')

        password_input = self.driver.find_element(By.ID, 'password')
        password_input.clear()
        password_input.send_keys('2ZM8KAvkKdTftm5')

        password_input.send_keys(Keys.ENTER)


        time.sleep(10)
        self.driver.get('https://loads.ati.su/#?filter={"firmListsExclusiveMode":false,"extraParams":64,"withAuction":false}')
        self.driver.refresh()



        # except Exception as e:
        #     print(e)


    def __paginator(self):
        self.driver.implicitly_wait(12)
        while self.driver.find_elements(By.CLASS_NAME, 'next_FJXnH') and self.count > 0 :
            self.__parse_page()
            button = self.driver.find_element(By.CLASS_NAME, 'next_FJXnH')
            self.driver.execute_script("arguments[0].click();", button)
            self.count -= 1
            print(f"Страниц спарсил {self.count} -----------------------------------------------------------------")

    def __parse_page(self):
        self.driver.implicitly_wait(12)
        titles = self.driver.find_elements(By.CLASS_NAME, "fOZ4h")


        for title in titles:
            try:
                title.find_element(By.CLASS_NAME, "[class='F7s7R']").click()
            except Exception as e:
                print(e)

            link = title.find_element(By.CSS_SELECTOR, "[class*='XfMtd fmVZ6']").get_attribute("href")

            data = {'link': link}

            # Получаем значение атрибута 'class'


            # Создаем объект BeautifulSoup для текущего элемента
            soup_title = BeautifulSoup(title.get_attribute("outerHTML"), 'html.parser')

            # Проводим поиск внутри soup_title
            number = soup_title.select_one("[class='ClIJE']")
            if number:
                data['number'] = number.text

            all_info = soup_title.select_one("[class='wO1Ia']")
            if all_info:
                all_info_text = all_info.text.replace('сайтеНаписать', ' ')
                data['info'] = all_info_text

            bid = soup_title.select_one("[class='Pai6y']")
            if bid:
                data['bid'] = bid.text

            route = soup_title.select_one("[class='NcNn7']")
            if route:
                data['route'] = route.text

            weight = soup_title.select_one("[class='OZttn']")
            if weight:
                data['weight'] = weight.text

            transport = soup_title.select_one("[class='qJ9Xx']")
            if transport:
                data['transport'] = transport.text

            direction = soup_title.select_one("[class='kPlZQ']")
            if direction:
                data['direction'] = direction.text

            self.data_list.append(data)
            df = pd.DataFrame(self.data_list)
            excel_file = 'cargoo.xlsx'

            with pd.ExcelWriter(excel_file, engine='xlsxwriter', mode='w') as writer:
                df.to_excel(writer, sheet_name='Sheet1', index=False)



    # def __save_data(self):
    #     df = pd.DataFrame(self.data_list)
    #     excel_file = 'cargo.xlsx'
    #
    #     with pd.ExcelWriter(excel_file, engine='xlsxwriter', mode='w') as writer:
    #         df.to_excel(writer, sheet_name='Sheet1', index=False)


    def parse(self):
        self.__set_up()
        self.__get_url()
        self.__paginator()
        self.__parse_page()
        # self.__save_data()

if __name__ == "__main__":
    AvitoPars(url='https://id.ati.su/login/'
              , count=180, item=['']).parse()








