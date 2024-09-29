from src.authors_crawler import AuthorCrawler
from src.poems_crawler import PoemCrawler
from src.elasticsearch_client import ElasticsearchClient
from config.settings import THIVIEN_URL

def main():
    author_crawler = AuthorCrawler(THIVIEN_URL)
    poem_crawler = PoemCrawler()
    elastic_client = ElasticsearchClient()

    # Bước 1: Crawl danh sách tác giả
    authors = author_crawler.crawl_authors(page_limit=3)

    # Bước 2: Crawl bài thơ của từng tác giả song song
    all_poem_links = []
    for author in authors:
        poem_links = author_crawler.crawl_poems_by_author(author['profile_url'])
        all_poem_links.extend(poem_links)

    # Bước 3: Crawl chi tiết từng bài thơ song song
    poems_data = poem_crawler.crawl_poems_parallel(all_poem_links, max_workers=10)

    # Bước 4: Lưu dữ liệu vào Elasticsearch
    status_code, response = elastic_client.bulk_insert(poems_data)

    if status_code == 200:
        print("Data successfully inserted into Elasticsearch.")
    else:
        print(f"Failed to insert data. Response: {response}")

if __name__ == "__main__":
    main()
