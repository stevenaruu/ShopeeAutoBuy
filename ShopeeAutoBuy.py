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

def AutoBuy(driver):
    # size button is optional, depend the market have an option or not
    size_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="42"]')))
    size_button.click()

    submit_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="beli sekarang"]')))
    submit_button.click()

    checkout_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//span[text()="checkout"]')))
    checkout_button.click()

    order_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Buat Pesanan"]')))
    order_button.click()

def SetupShopee(link_product):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)

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
            AutoBuy(driver)
    else:
        print("Cannot login")
        print("Try re-login")
        SetupShopee(link_product)

link_product = input('Shopee Product Link: ')
SetupShopee(link_product)

