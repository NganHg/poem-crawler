from src.poems_crawler import PoemCrawler
from src.utils import get_proxies
from config.settings import THIVIEN_URL, COUNTRY_CODE
import time
import random

def main():
    pl_crawler = PoemCrawler(THIVIEN_URL)
    links = pl_crawler.crawl_poem_all()
    # print(links)

if __name__ == "__main__":
    main()
