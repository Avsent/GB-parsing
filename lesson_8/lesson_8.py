from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import wget

chrome_options = Options()
chrome_options.add_argument("start-maximized")
driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)
driver.get("https://data.gov.ru/opendata")

data = WDW(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//a[@href="/opendata/7703771271-ekp"]')))
sleep(1)
data.click()

element = driver.find_element_by_xpath('//td/a[contains(text(), "Скачать")]')
url = element.get_attribute('href')
wget.download(url)