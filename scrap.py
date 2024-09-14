import time
from selenium.webdriver.common.by import By

class TwitterScraper:
    def __init__(self, driver):
        print("TwitterScraper")
        self.driver = driver



    def scrape_posts(self):
        print("scrape_posts")
        self.driver.get("https://x.com/explore")
        time.sleep(5)

        while True:
            time.sleep(10)
            print("while")
            # posts = self.driver.find_elements(By.XPATH, "//article")  # XPath برای یافتن تمام پست‌ها
            #
            # # باز کردن فایل برای ذخیره داده‌ها
            # with open("posts_data.txt", "a", encoding="utf-8") as file:
            #     for post in posts:
            #         try:
            #             # یافتن یوزرنیم
            #             username = post.find_element(By.XPATH, ".//header//span//a").text  # XPath برای یوزرنیم
            #             # یافتن متن پست
            #             text = post.find_element(By.XPATH, ".//div[2]/div[2]").text  # XPath برای متن پست
            #
            #             # ذخیره یوزرنیم و متن در فایل
            #             file.write(f"Username: {username}\n")
            #             file.write(f"Post Text: {text}\n")
            #             file.write("=" * 50 + "\n")  # جداکننده بین پست‌ها
            #
            #             print(f"Username: {username}, Post Text: {text}")
            #
            #         except Exception as e:
            #             print(f"Error extracting post: {e}")
                        # print("text")
                        # print(text)
                        # # استخراج لایک‌ها
                        # likes = post.find_element(By.XPATH, ".//div[2]/div[2]/div[2]/div[1]").text
                        # print("likes")
                        # print(likes)
                        # # استخراج کامنت‌ها
                        # comments = post.find_element(By.XPATH, ".//div[2]/div[2]/div[2]/div[2]").text
                        # print("comments")
                        # print(comments)
                        # # نوشتن داده‌ها به فایل
                    #     file.write(f"Text: {text}\n")
                    #     # file.write(f"Likes: {likes}\n")
                    #     # file.write(f"Comments: {comments}\n")
                    #     file.write("=" * 40 + "\n")  # جدا کننده برای خوانایی بهتر
                    #
                    # except Exception as e:
                    #     file.write(f"Error: {e}\n")
                    #     file.write("=" * 40 + "\n")


            # tweets = self.driver.find_elements(By.XPATH, "//article")  # یافتن تمام توییت‌ها
            #
            # # باز کردن فایل برای ذخیره داده‌ها
            # with open("tweets_data.txt", "a", encoding="utf-8") as file:
            #     for tweet in tweets:
            #         try:
            #             # یافتن نام کاربری
            #             username = tweet.find_element(By.XPATH, ".//div[@dir='ltr']//span").text  # XPath برای نام کاربری
            #
            #             # یافتن متن توییت
            #             text = tweet.find_element(By.XPATH, ".//div[@data-testid='tweetText']").text  # XPath برای متن توییت
            #
            #             # یافتن تعداد لایک‌ها
            #             try:
            #                 likes = tweet.find_element(By.XPATH, ".//div[@data-testid='like']//span").text  # XPath برای لایک‌ها
            #             except:
            #                 likes = "No likes visible"
            #
            #             # یافتن تعداد کامنت‌ها
            #             try:
            #                 comments = tweet.find_element(By.XPATH, ".//div[@data-testid='reply']//span").text  # XPath برای کامنت‌ها
            #             except:
            #                 comments = "No comments visible"
            #
            #             # ذخیره اطلاعات در فایل
            #             file.write(f"Username: {username}\n")
            #             file.write(f"Tweet Text: {text}\n")
            #             file.write(f"Likes: {likes}\n")
            #             file.write(f"Comments: {comments}\n")
            #             file.write("=" * 50 + "\n")  # جداکننده بین توییت‌ها
            #
            #             # چاپ اطلاعات برای دیباگ
            #             print(f"Username: {username}, Tweet Text: {text}, Likes: {likes}, Comments: {comments}")
            #         except Exception as e:
            #             print(f"Error extracting post: {e}")



            last_height = self.driver.execute_script("return document.body.scrollHeight")

            while True:
                tweets = self.driver.find_elements(By.XPATH, "//article")  # Locate all tweets

                with open("tweets_data.txt", "a", encoding="utf-8") as file:
                    for tweet in tweets:
                        try:
                            # Username
                            username = tweet.find_element(By.XPATH, ".//div[@dir='ltr']//span").text
                            # Tweet text
                            text = tweet.find_element(By.XPATH, ".//div[@data-testid='tweetText']").text

                            # Likes
                            try:
                                likes = tweet.find_element(By.XPATH, "//*[@id='id__ec5o2jlazzi']/div[1]/button/div/div[2]/span/span/span").text
                                print(likes)
                            except:
                                likes = "No likes visible"

                            # Comments
                            try:
                                comments = tweet.find_element(By.XPATH, ".//div[@data-testid='reply']//span").text
                            except:
                                comments = "No comments visible"

                            # Save data to file
                            file.write(f"Username: {username}\n")
                            file.write(f"Tweet Text: {text}\n")
                            file.write(f"Likes: {likes}\n")
                            file.write(f"Comments: {comments}\n")
                            file.write("=" * 50 + "\n")

                            print(f"Username: {username}, Tweet Text: {text}, Likes: {likes}, Comments: {comments}")
                        except Exception as e:
                            print(f"Error extracting tweet: {e}")

                # Scroll to load more tweets
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)

                # Check if page height has changed (to detect end of page)
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height



    def scrape_instagram(self):
        """اسکرول کردن صفحه و گرفتن اطلاعات پست‌ها"""
        for _ in range(10):  # اسکرول کردن صفحه به تعداد مشخص
            self.scroll_down(times=3)
            self.scrape_posts()