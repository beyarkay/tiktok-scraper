import scrapy
import sys
import datetime
from scrapy.linkextractors import LinkExtractor
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.selector import Selector
from shutil import which
  

class TikTokSpider(scrapy.Spider):
    name = "tiktok"
    start_urls = ['https://www.tiktok.com/foryou']
    CSS_TIKTOK = ".etvrc4k0"
    CSS_AUDIOS = ".epjbyn0 a"
    CSS_HEARTS = ".e1hk3hf90:nth-child(1) .e1hk3hf92"
    CSS_COMMTS = ".e1hk3hf90:nth-child(2) .e1hk3hf92"
    CSS_SHARES = ".e1hk3hf90:nth-child(3) .e1hk3hf92"
    CSS_USERS =  ".emt6k1z0"


    def __init__(self):
        scrapy.Spider.__init__(self)
        opts = FirefoxOptions()
        opts.add_argument("--headless")
        self.driver = webdriver.Firefox(options=opts)
        if not hasattr(self, 'min_tiktoks'):
            self.min_tiktoks = 30


    def __del__(self):
        try:
            self.driver.quit()
            scrapy.Spider.__del__(self)
        except AttributeError:
            print("no __del__ method exists in parent")

    def parse(self, response):
        self.logger.info("About to scrape from " + response.url)
        sel = Selector(response)
        self.driver.get(response.url)
        #wait for the iframe to load, beacuse the iframes are loaded via AJAX, after the initial page load

        def scroll_and_check(driver):
            driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
            num_tiktoks = len(driver.find_elements(by=By.CSS_SELECTOR, value=self.CSS_TIKTOK))
            if num_tiktoks % 25 == 0:
                self.logger.info(f"Scrapped {num_tiktoks}/{self.min_tiktoks} ({num_tiktoks/self.min_tiktoks * 100:.0f}%) tiptoes...")
            return num_tiktoks > self.min_tiktoks

        try:
            timeout = int(0.5 * self.min_tiktoks)
            self.logger.info(f"Waiting until {self.min_tiktoks} tiktoks are loaded or {timeout}s passed")
            WebDriverWait(self.driver, timeout, 2).until(scroll_and_check)
        except Exception as e:
            self.logger.info(f'Quitting driver, only {len(self.driver.find_elements(by=By.CSS_SELECTOR, value=self.CSS_TIKTOK))} tiktoks found. error: {e}')
            self.driver.quit()
            sys.exit(1)

        audios = [l.text for l in self.driver.find_elements(by=By.CSS_SELECTOR, value='.epjbyn0 a')]
        hearts = [l.text for l in self.driver.find_elements(by=By.CSS_SELECTOR, value='.e1hk3hf90:nth-child(1) .e1hk3hf92')]
        commts = [l.text for l in self.driver.find_elements(by=By.CSS_SELECTOR, value='.e1hk3hf90:nth-child(2) .e1hk3hf92')]
        shares = [l.text for l in self.driver.find_elements(by=By.CSS_SELECTOR, value='.e1hk3hf90:nth-child(3) .e1hk3hf92')]
        users =  [l.text for l in self.driver.find_elements(by=By.CSS_SELECTOR, value='.emt6k1z0')]

        for a, h, c, s, u in zip(audios, hearts, commts, shares, users):
            yield {
                'scraped_at': datetime.datetime.now(),
                'audio': a,
                'hearts': h,
                'commts': c,
                'shares': s,
                'user': u,
            }
