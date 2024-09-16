from login import Twitter
from  scrap import TwitterScraper
import time
from selenium import webdriver

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

if __name__ == '__main__':
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    Twitter("jhoseinzade1", "$Salam1234", driver).load_cookies_and_login()
    time.sleep(10)
    print("salam")
    TwitterScraper(driver).scrape_posts()


