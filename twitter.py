from login import Twitter
from  scrap import TwitterScraper
import time
from selenium import webdriver

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

if __name__ == '__main__':
    options = Options()
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    Twitter("jhoseinzade1", "$Salam1234", driver).load_cookies_and_login()
    time.sleep(10)
    print("salam")
    TwitterScraper(driver).scrape_posts()


