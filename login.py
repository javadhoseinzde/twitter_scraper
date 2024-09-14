import time
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.safari.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Twitter:
    def __init__(self, username, password, driver):
        self.username = username
        self.password = password
        self.driver = driver


    def login(self):


        url = "https://twitter.com/i/flow/login"
        self.driver.get(url)

        WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="username"]'))).send_keys(
            self.username)
        self.driver.find_element(By.CSS_SELECTOR, 'input[autocomplete="username"]').send_keys(Keys.ENTER)

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="password"]'))).send_keys(self.password)
        self.driver.find_element(By.CSS_SELECTOR, 'input[name="password"]').send_keys(Keys.ENTER)

        # Wait for the home page to load
        WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="AppTabBar_Home_Link"]')))
        print("Login successful.")

        # Save cookies to a file
        with open("cookies.pkl", "wb") as cookies_file:
            pickle.dump(self.driver.get_cookies(), cookies_file)
        print("Cookies saved.")
        time.sleep(5)

    def handle_cookie_consent(self):
        try:
            # Look for the cookie consent button and click it
            consent_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Accept")]'))
            )
            consent_button.click()
            print("Cookie consent accepted.")
        except Exception as e:
            print("No cookie consent dialog found or error:", e)

    def load_cookies_and_login(self):

        url = "https://twitter.com"
        self.driver.get(url)

        # Handle cookie consent if it appears
        self.handle_cookie_consent()

        # Load cookies from file
        try:
            with open("cookies.pkl", "rb") as cookies_file:
                cookies = pickle.load(cookies_file)
                for cookie in cookies:
                    if 'sameSite' in cookie:
                        cookie.pop('sameSite')
                    if 'expiry' in cookie:
                        cookie['expiry'] = int(cookie['expiry'])
                    self.driver.add_cookie(cookie)
            print("Cookies loaded.")
            self.driver.refresh()
            time.sleep(5)
            print("Login successful.")
        except FileNotFoundError:
            print("Cookies not found. Performing login manually.")
            self.login()

