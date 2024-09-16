import time
from selenium.webdriver.common.by import By
from mongo_connection.mongo_connection import MongoConnection
from utils.split_username import split_username


class TwitterScraper:
    def __init__(self, driver):
        print("TwitterScraper")
        self.driver = driver

    def scrap_comments(self, link):
        self.driver.get(link)

        print("after scrap comments")

        return

    def scrape_posts(self):
        print("scrape_posts")
        # self.driver.get("https://x.com/explore")

        while True:

            last_height = self.driver.execute_script("return document.body.scrollHeight")

            tweets = self.driver.find_elements(By.XPATH, "//article")  # Locate all tweets


            for tweet in tweets:
                try:
                    # Username
                    username = tweet.find_element(By.XPATH, ".//div[@data-testid='User-Name']").text
                    user = split_username(username)
                    # Tweet text
                    text = tweet.find_element(By.XPATH, ".//div[@data-testid='tweetText']").text

                    # Likes
                    try:
                        likes = tweet.find_element(By.XPATH,'.//button[@data-testid="like"]//span').text

                    except:
                        likes = "No likes visible"

                    # Comments
                    try:
                        comments = tweet.find_element(By.XPATH, './/button[@data-testid="reply"]//span').text
                    except:
                        comments = "No comments visible"
                    tweet_link = tweet.find_element(
                        "xpath",
                        ".//a[contains(@href, '/status/')]",
                    ).get_attribute("href")
                    tweet_id = str(tweet_link.split("/")[-1])
                    print("_______________")
                    print(tweet_id)
                    print(tweet_link)
                    print("_______________")
                    json_data = {
                        "username":user,
                        "tweet Text":text,
                        "likes":likes,
                        "comments":comments
                    }
                    MongoConnection("localhost",
                                    27017,
                                    "root",
                                    "example").insert_data("Twitter-test", json_data)

                    time.sleep(2)
                except Exception as e:
                    print(f"Error extracting tweet: {e}")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")





