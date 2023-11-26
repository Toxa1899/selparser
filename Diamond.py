import json
import time
import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup
import pandas as pd


class WebParser:
    def __init__(self, url: str, count = 10):
        self.url = url

        self.count = count
        self.data = []
        self.txt_description = []


    def __set_up(self):

        self.driver = webdriver.Chrome()


    def __get_url(self):
        # self.driver.get(self.url)

        try:
            self.driver.maximize_window()
            self.driver.get(self.url)
            self.driver.implicitly_wait(9)
            account_icon = self.driver.find_element(By.ID, "Account")
            account_icon.click()

            login_input = self.driver.find_element(By.CSS_SELECTOR, "[data-test='username']")
            login_input.clear()
            login_input.send_keys('hildasauctionhouse')

            password_input = self.driver.find_element(By.CSS_SELECTOR, "[data-test='password']")
            password_input.clear()
            password_input.send_keys('Hilda1964')
            password_input.send_keys(Keys.ENTER)

        except Exception as e:
            print(e)


    def __paginator(self):
        time.sleep(4)
        while self.driver.find_element(By.CSS_SELECTOR, "[data-icon='caret-right']") and self.count > 1:
            time.sleep(5)
            self.__parser()
            time.sleep(3)
            next_page_button = self.driver.find_element(By.CSS_SELECTOR, "[data-icon='caret-right']")
            self.driver.execute_script("arguments[0].scrollIntoView(true);", next_page_button)
            ActionChains(self.driver).move_to_element(next_page_button).click().perform()
            self.count -= 1

    def __parser(self):
        time.sleep(8)
        title = self.driver.find_elements(By.CSS_SELECTOR,
                                          "[class*='productResultCard px-0 px-sm-1 mb-sm-3 mb-0 u-flex-grid-col-xl-3 u-flex-grid-col-lg-4 u-flex-grid-col-sm-6 col-12']")

        # Создаем пустой список для хранения данных
        all_data = []

        for titles in title:
            self.driver.implicitly_wait(9)
            link = titles.find_element(By.CSS_SELECTOR, "[class='productCardDesc stretched-link']").get_attribute(
                "href")

            ActionChains(self.driver).key_down(Keys.CONTROL).click(titles).key_up(Keys.CONTROL).perform()

            self.driver.implicitly_wait(9)
            self.driver.switch_to.window(self.driver.window_handles[-1])

            product = self.driver.find_elements(By.ID, "productModelBindingKey")


            for product_text in product:
                name = product_text.find_element(By.CLASS_NAME, 'productDescription').text


                vendor_code = product_text.find_element(By.CSS_SELECTOR, "[data-test='item-number']").text


                html = self.driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                price_element = soup.select_one("[data-test='usd-price']")
                price_text = price_element.text if price_element else None



                image = soup.select("[data-type='image']")
                sinta_image = [image.get('href') for image in image]
                str_img = ",".join(sinta_image)

                description_element = soup.select("[class='topMarginExtraLarge']")

                # Создаем новый экземпляр data_dict
                data_dict = {'name': name,
                             'link': link,
                             'vendor_code': vendor_code,
                             'price_text': price_text,
                             'str_img': str_img,
                             'description': '',
                             }

                for description_element in description_element:
                    h3_element = description_element.find('h3')
                    if h3_element:
                        category_name = h3_element.text.strip()
                        category_data = {}

                        # Найти все td элементы внутри текущего элемента description
                        td_elements = description_element.find_all('td')

                        for i in range(0, len(td_elements), 2):  # Перебор каждой пары td элементов
                            key = td_elements[i].text.strip()
                            value = td_elements[i + 1].text.strip()
                            category_data[key] = value


                        data_dict['description'] = category_data



                # Добавляем в список all_data
                all_data.append(data_dict)
                print(all_data)

            # Закрываем текущее окно
            self.driver.close()
            # Переключаемся на первое окно
            self.driver.switch_to.window(self.driver.window_handles[0])


            df = pd.DataFrame(all_data)
            excel_file = 'Diamondsss.xlsx'

            with pd.ExcelWriter(excel_file, engine='xlsxwriter', mode='w') as writer:
                df.to_excel(writer, sheet_name='Sheet1', index=False)

        # Закрываем браузер
        self.driver.close()


    # def save_date(self):
    #     with open('diamond.json', 'w', encoding='utf-8')as f:
    #         json.dump(self.data, f , ensure_ascii=False, indent= 6)
    #





    def pars(self):
        self.__set_up()
        self.__get_url()
        self.__paginator()
        self.__parser()
        # self.save_date()


if __name__ == "__main__":
    WebParser(url='https://www.stuller.com/browse/jewelry/earrings/diamond-studs', count=2).pars()
