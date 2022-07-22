import scrapy
import datetime
from scrapy.linkextractors import LinkExtractor
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.selector import Selector
from shutil import which
  
SELENIUM_DRIVER_NAME = 'firefox'
SELENIUM_DRIVER_EXECUTABLE_PATH = which('geckodriver')
SELENIUM_DRIVER_ARGUMENTS=['-headless']


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
        # using a firefox driver
        self.driver = webdriver.Firefox()

    def __del__(self):
        try:
            self.driver.quit()
            scrapy.Spider.__del__(self)
        except AttributeError:
            print("no __del__ method exists in parent")

    def parse(self, response):
        self.logger.info("This url has been identified - " + response.url)
        sel = Selector(response)
        self.driver.get(response.url)
        #wait for the iframe to load, beacuse the iframes are loaded via AJAX, after the initial page load
        self.logger.info("Got URL, sleeping")
        min_elements = 500
        self.logger.info("Attempting to load TikToks")

        def scroll_and_check(driver):
            driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
            return len(driver.find_elements(by=By.CSS_SELECTOR, value=self.CSS_TIKTOK)) > min_elements

        try:
            WebDriverWait(self.driver, 60).until(scroll_and_check)
        except Exception:
            self.logger.info(f'Quitting driver, only {len(self.driver.find_elements(by=By.CSS_SELECTOR, value=self.CSS_TIKTOK))} tiktoks found')
            self.driver.quit()


        audios = [l.text for l in self.driver.find_elements(by=By.CSS_SELECTOR, value='.epjbyn0 a')]
        hearts = [l.text for l in self.driver.find_elements(by=By.CSS_SELECTOR, value='.e1hk3hf90:nth-child(1) .e1hk3hf92')]
        commts = [l.text for l in self.driver.find_elements(by=By.CSS_SELECTOR, value='.e1hk3hf90:nth-child(2) .e1hk3hf92')]
        shares = [l.text for l in self.driver.find_elements(by=By.CSS_SELECTOR, value='.e1hk3hf90:nth-child(3) .e1hk3hf92')]
        users =  [l.text for l in self.driver.find_elements(by=By.CSS_SELECTOR, value='.emt6k1z0')]

        def parse_formatted_numeric(n: str) -> int:
            if n[-1] == "M":
                return int(float(n[:-1]) * 1_000_000)
            elif n[-1] == "K":
                return int(float(n[:-1]) * 1_000)
            else:
                return int(n)

        for a, h, c, s, u in zip(audios, hearts, commts, shares, users):
            yield {
                'scraped_at': datetime.datetime.now(),
                'audio': a,
                'hearts': parse_formatted_numeric(h),
                'commts': parse_formatted_numeric(c),
                'shares': parse_formatted_numeric(s),
                'user': f'https://www.tiktok.com/@{u}',
            }
