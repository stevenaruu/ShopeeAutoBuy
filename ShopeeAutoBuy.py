from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
from dotenv import load_dotenv

load_dotenv()
LOGIN_VALUE = os.getenv("LOGIN_VALUE")
PASSWORD_VALUE = os.getenv("PASSWORD_VALUE")

def AutoRefresh(driver, time_input):
    while True:
        current_time = time.localtime()

        current_hour = current_time.tm_hour
        current_minute = current_time.tm_min
        current_second = current_time.tm_sec

        target_hour = int(time_input[0])
        target_minute = int(time_input[1])
        target_second = int(time_input[2])

        print(f"Current Time: {current_hour:02d}:{current_minute:02d}:{current_second:02d}")

        if(target_hour >= current_hour and target_minute >= current_minute and target_second >= current_second):
            return

        driver.refresh()

def AutoBuy(driver):
    # size button is optional, depend the market have an option or not (variant)
    size_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="42"]')))
    size_button.click()

    submit_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="beli sekarang"]')))
    submit_button.click()

    checkout_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//span[text()="checkout"]')))
    checkout_button.click()

    order_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Buat Pesanan"]')))
    actions = ActionChains(driver)
    actions.move_to_element(order_button).perform()
    order_button.click()

def SetupShopee(link_product, time_input):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_argument("--start-maximized") 

    driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
    driver.get("https://shopee.co.id/buyer/login")

    login = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "loginKey")))
    login.send_keys(LOGIN_VALUE)

    password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "password")))
    password.send_keys(PASSWORD_VALUE)

    login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div/div[2]/div/div/div/div[2]/form/div/div[2]/button')))
    login_button.click()

    success = WebDriverWait(driver, 10).until(EC.url_to_be("https://shopee.co.id/?is_from_login=true"))

    if(success):
        print("Login success")
        driver.get(link_product)
        
        wait = WebDriverWait(driver, 10).until(EC.url_to_be(link_product))
        
        if(wait):
            AutoRefresh(driver, time_input)
            AutoBuy(driver)
    else:
        print("Cannot login")
        print("Try re-login")
        SetupShopee(link_product)

link_product = input('Shopee Product Link: ')
hour = input('Input Hour: ')
minute = input('Input Minute: ')
second = input('Input Second: ')

time_input = [hour, minute, second]

SetupShopee(link_product, time_input)