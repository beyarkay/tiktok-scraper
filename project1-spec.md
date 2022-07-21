# Project 1 - Scraping and data processing

Principles of Data Science - CS746

**Due: 14 August @ 24h00.**

## Project description:
Web scraping is the process of collecting data from web resources. Data from
web resources can be structured (for example data made available through APIs),
semi-structured, or unstructured (e.g., videos, blog and social media posts,
etc...). Most frequently the data available on the web is semi-structured since
it does not follow the format of a tabular data model or relational databases
(i.e., it does not have a fixed schema). However, the data is often embedded in
HTML code, which can help to identify properties of the data.

For this project you are required to implement a web scraper using the [Scrapy
library](https://scrapy.org/) to scrape semi-structured data from websites and
process the data into well-structued data. You will analyse the scraped data to
answer some questions and report on your findings.

## About `Scrapy`

Please install `Scrapy` by following [these
guidelines](https://docs.scrapy.org/en/latest/intro/install.html). It is
recommended to install `Scrapy` in a [virtual
environment](https://docs.python.org/3/tutorial/venv.html#tut-venv) and do not
use `python-scrapy` that comes with the Ubuntu package repository. 

`Scrapy` is designed with a versatile and extensible architecture.
![scrapy_architecture.png](scrapy_architecture.png)

Please read [this
document](https://docs.scrapy.org/en/latest/topics/architecture.html) to
fimilarise yourself with the architecture and how the various components
interact with each other. At minimum, you will need to implement a spider and
parser (7), itmes that are passed around, and one pipeline component. You will
most likely enable some Middleware component and depending on your use case,
you might also need to implement a custom request object.

## Implementation details and requirements:

You can get started with `Scrapy` by working through [this
tutorial](https://docs.scrapy.org/en/latest/intro/tutorial.html#intro-tutorial).
However, the tutorial only executes `Scrapy` directly from the command line. If
you want to call your crawler from a your own `__main__` program use the code
given below:

```python
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

my_settings = {
    ### dictionary of optional settings
}

if __name__ == '__main__':

    process = CrawlerProcess(get_project_settings())
    process.crawl('MyScraper',
                  custom_settings=my_settings)
    process.start()
```

### Implementation requirements:
1. **Scrapy Items:** You are required to define and use your own [Scrapy
   Items](https://doc.scrapy.org/en/latest/topics/items.html). The number of
   custom `Items` and their `Fields` is up to you and largly depends on your
   use case. All custom `Items` implementations should be in the file named
   `items.py`.

2. **Item Pipeline:** You should also implement an [Item
   Pipeline](https://docs.scrapy.org/en/latest/topics/item-pipeline.html) that
   processes your scraped `Items`. Again, the number of pipeline components you
   implement is up to you and depends on the use case and your pipeline design.
   All pipeline components should be in the file named `pipelines.py`.

3. **Database Pipeline:** Your Scrapy pipeline needs to implement a pipeline
   component that is used to store your structured data into some external data
   storage. Options are (from easy to difficult):
   - a csv file
   - using the filesystem structure
   - a `Postgres` database

4. **Settings:** Your crawler's settings should be specified in the
   `settings.py` file of your project. Important settings to consider in order
   for your crawler to behave nicely are:
   - For following links: `REDIRECT_ENABLED`, `ROBOTSTXT_OBEY`
   - For playing nice: `AUTOTHROTTLE_TARGET_CONCURRENCY`, `AUTOTHROTTLE_ENABLED`, (see the [AutoThrottle extension](https://doc.scrapy.org/en/latest/topics/autothrottle.html) for Scrapy)
   - For downloading files: `RANDOMIZE_DOWNLOAD_DELAY`, `DOWNLOAD_DELAY`.

5. **GitLab:** You are required to use a GitLab repository for this project.
   You should have access to a repository under `Computer-Science -> Data
   Science -> 2022 -> Projects -> <student_nr> rw746 Data Science Project 1 `
   with your student number as repository name. The repository should have the
   following folder structure:
```
    src/
    report/
    data/
```
where the folder `data` contains the cleaned well-structured data collected
from your scrape, `report/` contains your report in PDF format, and `src/`
contain the source files for your `Scrapy` crawler.

6. **Selectors:** You may use any of the [build-in
   selectors](https://docs.scrapy.org/en/latest/topics/selectors.html): XPath
   or CSS. For the brave that want to work with the [Selenium
   middleware](https://github.com/clemfromspace/scrapy-selenium), you might
   have additional options to scrape data.


## What should you scrape?
This is pretty much up to you as long as you follow the implementation
requirements. I encourage you to take your time and look for interesting data
out there before starting your implementation. Before you decide on which
website and data to scrape, consider the following:

- Will you be able to answer some interesting questions with the data?
- Can you define a resonable search scope for your crawler? You don't want to
  crawl the entire Amazon website, for example.
- On the flip side, you don't want to only crawl a handful of pages. The data
  you collect should be distributed over many pages in order for your spider to
  stretch it legs.
- Is the data you want to scrape dynamic? It might require you to use the
  Selenium middleware to handle javascript pages.
- What are the access restrictions of the site? Will you be blocked or required
  to solve reCaptchas? If yes, can you throttle the crawler's access frequency
  sufficiently to not get blocked and still scrape all the required data?

Some not particularily good ideas of websites to crawl:

* https://www.property24.com/ (has interesting data)
* https://www.gov.za/document/latest (the data to scape is mostly text and
  PDFs, but this data could be useful for later projects when applying NLP
  techniques)
* https://scholar.sun.ac.za/
* Reddit: You can look for an interesting subreddit and crawl it.
* https://www.news24.com/ (note: many articles are behind a paywall)
* Some well-defined subset of items in https://www.worldcat.org/ (note: the
  website contains JavaScript elements).
* https://sajs.co.za/issue/archive


## Report requirements:
Your report should have the following sections:
1. **Introduction:** Short introduction: the why, the how, the achieved scrape
   results, the main findings from the data.
2. **Implementation:** Brief overview of your particular implementation.
3. **Crawl process:** Description of the crawl process.
4. **Data scraped:** High-level description of the data that was scraped. Can
   you give an indication of the percentage of data that was scraped compared
   to all available data?
5. **Results** (answers to questions)

Sections 1 through 4 should not take up more than two pages in total. Section 5
may be longer depending on the graphs and figures you generate from the data.
Each graph should be meaningful and be described concisely.

### Considerations for achieving a good mark:
* In addition to scraping unstructured data from HTML you also download files
  (PDFs, XML documents, images, etc...) that are processed in your pipeline.
  Please do not add GBs of data to your GitLab repository. Only upload your
  cleaned and processed data which you used to generate the results in your
  report. If you downloaded large amounts of data and plan on using it for
  later projects please contact me directly.
* A well-written and concise report.
* Interesting use-case and questions.
* Good answeres from the scraped data with well designed graphs or figures.
  Note, we do not expect you to do complex analysis on the data (that comes
  later in the course).

## Resources:
* [Scrapy Documentation](https://docs.scrapy.org/en/latest/)
