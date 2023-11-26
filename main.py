# coding: UTF-8
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
# Setup Chrome options
options = Options()
# options.add_argument("--headless") # Ensure GUI is off. Remove this line if you want to see the browser navigating.

# Set path to chromedriver as a service
webdriver_service = Service(ChromeDriverManager().install())

# Set the driver
driver = webdriver.Chrome(service=webdriver_service, options=options)

# Get website data
driver.get("https://www.instagram.com")

# Take a screenshot
driver.save_screenshot("screenshot.png")

time.sleep(5)
# Quit the driver
driver.quit()
