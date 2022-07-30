import scrapy
from time import sleep
from time import time
import sys
import datetime
from scrapy.linkextractors import LinkExtractor
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from scrapy.selector import Selector
from shutil import which
  

class TikTokSpider(scrapy.Spider):
    name = "tiktok"
    start_urls = ['https://www.tiktok.com/foryou']
    CSS_VIDEO  = ".e1yey0rl0"
    CSS_USER_PROFILE = '.er095117'

    def __init__(self):
        scrapy.Spider.__init__(self)
        opts = FirefoxOptions()
        self.is_headless = True
        if self.is_headless:
            opts.add_argument("--headless")
        self.driver = webdriver.Firefox(options=opts)
        self.min_tiktoks = 100


    def __del__(self):
        try:
            self.driver.quit()
            scrapy.Spider.__del__(self)
        except AttributeError:
            self.logger.info("Finishing")

    def parse(self, response):
        sel = Selector(response)
        self.logger.info(f"Getting URL {response.url}")
        self.driver.get(response.url)
        self.logger.info("Loaded, finding first video and clicking")
        self.driver.find_element(by=By.CSS_SELECTOR, value=self.CSS_VIDEO).click()
        sleep(1)

        num_tiktoks = 0
        while num_tiktoks < self.min_tiktoks:
            self.logger.info("Finding video...")
            try:
                start = time()
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.e1mecfx00')))
                curr_vid = self.driver.find_element(by=By.CSS_SELECTOR, value='.e1mecfx00')

                audio = curr_vid.find_element(by=By.CSS_SELECTOR, value='.epjbyn0 a')

                likes = curr_vid.find_element(by=By.CSS_SELECTOR, value='.e1hk3hf90:nth-child(1) .e1hk3hf92').text

                comments = curr_vid.find_element(by=By.CSS_SELECTOR, value='.e1hk3hf90:nth-child(2) .e1hk3hf92').text

                username = curr_vid.find_element(by=By.CSS_SELECTOR, value='.evv7pft1')
                ActionChains(self.driver).move_to_element(username).perform()

                self.logger.info(f"Waiting for user profile preview to be visible...")
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, self.CSS_USER_PROFILE)))
                WebDriverWait(self.driver, 20).until(lambda d: '--' not in d.find_element(by=By.CSS_SELECTOR, value='.er095117').text)
                user_followers, user_likes = self.driver.find_element(by=By.CSS_SELECTOR, value='.er095117').text.replace("Likes", "").split("Followers")
                self.logger.info(f"{audio.text=} {likes=} {username.text=} {comments=} {user_followers=} {user_likes=}")

                yield {
                    'scraped_at': datetime.datetime.now(),
                    'url': self.driver.current_url.replace("?is_copy_url=1&is_from_webapp=v1", ""),
                    'audio': audio.text,
                    'audio_url': audio.get_property("href"),
                    'likes': likes,
                    'comments': comments,
                    'username': username.text,
                    'user_followers': user_followers,
                    'user_likes': user_likes,
                }
                num_tiktoks += 1
            except Exception as e:
                self.logger.exception(e)

            self.logger.info(f"Pressing down arrow")
            old_url = self.driver.current_url
            self.logger.info(f"  Found body")
            body = self.driver.find_element(by=By.CSS_SELECTOR, value='body')
            limit = 20
            while old_url == self.driver.current_url:
                self.logger.info(f"  Sending down arrow, attempt {21 - limit}")
                body.send_keys(Keys.ARROW_DOWN)
                self.logger.info(f"  Sleeping")
                sleep(1)
                limit -= 1
                # If we can't find more tiktoks for some reason, just exit and
                # use what we've got
                if limit == 0:
                    self.logger.info(f"Failed to go to the next tiktok, restarting with {num_tiktoks} tiktoks")
                    self.driver.get(response.url)
                    self.logger.info("Loaded, finding first video and clicking")
                    self.driver.find_element(by=By.CSS_SELECTOR, value=self.CSS_VIDEO).click()
                    sleep(1)
            self.logger.info(f"Scraped {num_tiktoks}/{self.min_tiktoks} ({num_tiktoks/self.min_tiktoks * 100:.0f}%) tiktoks (took {time() - start}s)\n")
