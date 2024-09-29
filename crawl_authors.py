from src.authors_crawler import AuthorCrawler
from src.utils import get_proxies
from config.settings import THIVIEN_URL, COUNTRY_CODE
import time
import random

def main():
    for country in COUNTRY_CODE:
      author_crawler = AuthorCrawler(THIVIEN_URL, country)
      author_crawler.crawl_authors_all()
      time.sleep(random.uniform(1, 3))

if __name__ == "__main__":
    main()
