from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
from dotenv import load_dotenv

load_dotenv()
LOGIN_VALUE = os.getenv("LOGIN_VALUE")
PASSWORD_VALUE = os.getenv("PASSWORD_VALUE")

def setupShopee():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
    driver.get("https://shopee.co.id/buyer/login")

    login = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.NAME, "loginKey")))
    login.send_keys(LOGIN_VALUE)

    password = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.NAME, "password")))
    password.send_keys(PASSWORD_VALUE)

    login_button = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div/div[2]/div/div/div/div[2]/form/div/div[2]/button')))
    login_button.click()

setupShopee()

