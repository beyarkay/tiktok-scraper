# Scraping TikTok for fun and profit

This project contains all the code to scrape [TikTok](https://www.tiktok.com/),
analyse that data, and write a report on the findings.

## Installing requirements

To install the requirements for this project:

1. create a virtual environment:

    ```sh
    python3 -m venv .venv && source .venv/bin/activate
    ```

2. install the python requirements:
    ```sh
    pip install -r requirements.txt
    ```

3. install [FireFox](https://www.mozilla.org/en-US/firefox/new/) *AND*
   [`geckodriver`](https://github.com/mozilla/geckodriver/releases)

## Running the scraper interactively

There are two ways to run the scraper. The first is a once-off, and is as
simple as running the spider:

```sh
cd src && scrapy crawl tiktok
```

You should see a bunch of output scrolling by. This will scrape 100 tiktoks and
then stop. You can change that number by modifying line 31 in the
`tiktok_spider`:

```
$ rg "self.min_tiktoks = " src
src/tiktok_downloader/spiders/tiktok_spider.py
31:        self.min_tiktoks = 100
```

## Running the scraper in headless mode

The scraper can also be setup to run via a cronjob, although this process is a
bit more involved.

0. Create a directory to store the cron job's script:

```
mkdir ~/cronjobs
```

1. Soft link the script `src/tiktok_scraper.cron` to `~/cronjobs/tiktok_scraper.cron`

```
ln -s src/tiktok_scraper.cron ~/cronjobs/tiktok_scraper.cron
```

2. modify your cron via `crontab -e` to include a line like the following at
   the bottom:
```
# m h  dom mon dow   command
0 * * * * ~/cronjobs/tiktok_scraper.cron >> /home/brk/cronjobs/tiktok_scraper.log 2>&1
```

3. Everything should work now, and the crawler should run once an hour. It will
   kill any existing geckodriver processes before it starts creating new ones
   to make sure you don't end up with a million of them.

## Directory structure

```
├── README.md
├── data
│   └── tiktoks.jsonlines
├── project1-spec.md
├── report
│   ├── build_report.sh
│   ├── cite.bib
│   ├── img
│   │   ├── bellapoarch.png
│   │   ├── khaby.lame.png
│   │   ├── tiktok.png
│   ├── report.md
├── requirements.txt
└── src
    ├── analyse_data.ipynb
    ├── geckodriver.log
    ├── scrapy.cfg
    ├── tiktok_downloader
    │   ├── __init__.py
    │   ├── __pycache__
    │   ├── items.py
    │   ├── middlewares.py
    │   ├── pipelines.py
    │   ├── settings.py
    │   └── spiders
    └── tiktok_scraper.cron
``
