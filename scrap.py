import time

from selenium.webdriver.common.by import By

from mongo_connection.mongo_connection import MongoConnection
from utils.split_username import split_username


class TwitterScraper:
    def __init__(self, driver):
        print("TwitterScraper")
        self.driver = driver

    def scrap_comments(self):
        self.driver.get("https://x.com/arbabkohestan/status/1835731849689079867")

        message = "after scrap comments"

        return message

    def scrape_posts(self):
        mongo = MongoConnection()
        print("scrape_posts")
        # self.driver.get("https://x.com/explore")

        while True:
            last_height = self.driver.execute_script(
                "return document.body.scrollHeight"
            )

            tweets = self.driver.find_elements(By.XPATH, "//article")

            for tweet in tweets:
                try:
                    # Username
                    username = tweet.find_element(
                        By.XPATH, ".//div[@data-testid='User-Name']"
                    ).text
                    user = split_username(username)
                    # Tweet text
                    text = tweet.find_element(
                        By.XPATH, ".//div[@data-testid='tweetText']"
                    ).text

                    # Likes
                    try:
                        likes = tweet.find_element(
                            By.XPATH, './/button[@data-testid="like"]//span'
                        ).text

                    except:
                        likes = "No likes visible"

                    # Comments
                    try:
                        comments = tweet.find_element(
                            By.XPATH, './/button[@data-testid="reply"]//span'
                        ).text
                    except:
                        comments = "No comments visible"
                    tweet_link = tweet.find_element(
                        "xpath",
                        ".//a[contains(@href, '/status/')]",
                    ).get_attribute("href")
                    tweet_id = str(tweet_link.split("/")[-1])

                    json_data = {
                        "username": user,
                        "tweet Text": text,
                        "likes": likes,
                        "comments": comments,
                        "tweet id": tweet_id,
                        "tweet link": tweet_link,
                    }
                    mongo.insert_data(
                        db="twitter", collection_name="sep-2024-home", data=json_data
                    )

                except Exception as e:
                    print(f"Error extracting tweet: {e}")
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            time.sleep(5)

            # Check if page height has changed (to detect end of page)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
