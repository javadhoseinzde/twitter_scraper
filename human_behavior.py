import time
import random
import time
from datetime import datetime

class Personality_Type:
    
	def __init__(self):
		print("start init func")

	def post_type(self):
		pass

	def sleep_scrap(self):
		sleep_time = random.uniform(1300, 4200)
		print(f"Sleeping for {sleep_time / 60:.2f} minutes.")
		time.sleep(sleep_time)
  
  
	def sleep_time(self):
		now_time = str(datetime.now().strftime("%H"))
		if now_time > "21" and now_time < "7":
			return True


	def wakeup_time(self):
		now_time = str(datetime.now().strftime("%H"))
		if now_time > "7" and now_time < "21":
			return True


	def create_post(self):
		pass



class HumanBehavior:
	def __init__(self, driver):
		self.driver = driver

	def like_post(self, post):
		print(post)
		pass

	def sleep(self):
		pass

	def wakeup(self):
		pass

	def create_tweet(self):
		pass



# like_button = tweet.find_element(By.XPATH, './/button[@data-testid="like"]')
# like_button.click()
# time.sleep(10)