import logging

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from mongo_connection.mongo_connection import MongoConnection
from utils.split_username import split_username

logging.basicConfig(level=logging.INFO)

from human_behavior import HumanBehavior, Personality_Type
import time

class TwitterScraper:
    def __init__(self, driver):
        self.driver = driver
        self.scraped_tweet_ids = set()
        self.mongo = MongoConnection()

    def scrape_posts(
        self, collection_name="sep-2024-home", scroll_attempts=5, batch_size=10
    ):

        logging.info("Starting scrape_posts")

        attempts = 0
        tweets_batch = []

        while True:
            print("before check")
            # if Personality_Type().wakeup_time():
                
            last_height = self.driver.execute_script(
                "return document.body.scrollHeight"
            )

            try:
                WebDriverWait(self.driver, 60).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//article"))
                )

                tweets = self.driver.find_elements(By.XPATH, "//article")

                new_tweets_found = False

                #این قسمت شفاف شده
                for tweet in tweets:
                    try:
                        # Extract tweet ID to check if it's new
                        tweet_link = tweet.find_element(
                            "xpath", ".//a[contains(@href, '/status/')]"
                        ).get_attribute("href")
                        tweet_id = str(tweet_link.split("/")[-1])

                        if tweet_id not in self.scraped_tweet_ids:
                            new_tweets_found = True
                            self.scraped_tweet_ids.add(tweet_id)

                            # Extract relevant information
                            username = tweet.find_element(
                                By.XPATH, ".//div[@data-testid='User-Name']"
                            ).text
                            user = split_username(username)

                            text = tweet.find_element(
                                By.XPATH, ".//div[@data-testid='tweetText']"
                            ).text

                            # Likes
                            try:
                                likes = tweet.find_element(
                                    By.XPATH, './/button[@data-testid="like"]//span'
                                ).text
                            except NoSuchElementException:
                                likes = "No likes visible"

                            # Comments
                            try:
                                comments = tweet.find_element(
                                    By.XPATH, './/button[@data-testid="reply"]//span'
                                ).text
                            except NoSuchElementException:
                                comments = "No comments visible"

                            retweet_cnt = tweet.find_element(
                                By.XPATH, './/button[@data-testid="retweet"]//span'
                            ).text

                            json_data = {
                                "username": user,
                                "tweet Text": text,
                                "likes": likes,
                                "comments": comments,
                                "tweet id": tweet_id,
                                "tweet link": tweet_link,
                                "retweet": retweet_cnt,
                                "action": "tweet",
                            }
                            likes_button = tweet.find_element(
                                By.XPATH, './/button[@data-testid="like"]'
                            )

                            HumanBehavior(self.driver).like_post("post")
                            tweets_batch.append(json_data)


                            if len(tweets_batch) >= batch_size:
                                self._insert_batch(tweets_batch, collection_name)
                                tweets_batch.clear()
                    except Exception as e:
                        logging.error(f"Error extracting tweet: {e}")

                if new_tweets_found:
                    attempts = 0
                else:
                    attempts += 1
                    logging.info(
                        f"No new tweets found, attempt {attempts}/{scroll_attempts}"
                    )

                self.driver.execute_script("window.scrollBy(0, 1000);")

                WebDriverWait(self.driver, 10).until(
                    lambda driver: driver.execute_script(
                        "return document.body.scrollHeight"
                    )
                    > last_height
                )
            except TimeoutException as e:
                logging.warning("Timeout occurred, increasing timeout and retrying...")

                WebDriverWait(self.driver, 60).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//article"))
                )
                # Personality_Type.sleep_scrap()
                # self.driver.get("https://x.com")

            # else:
            #     print("sleeping")
            #     time.sleep(100)   
                
        if tweets_batch:
            self._insert_batch(tweets_batch, collection_name)
        logging.info("Scraping complete")

    def _insert_batch(self, tweets_batch, collection_name):
        try:
            for tweet in tweets_batch:
                self.mongo.insert_data(
                    db="twitter", collection_name=collection_name, data=tweet
                )
                    
            logging.info(f"Inserted {len(tweets_batch)} tweets into MongoDB.")
        except Exception as e:
            logging.error(f"Error inserting data into MongoDB: {e}")
