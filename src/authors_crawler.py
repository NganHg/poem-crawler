import os
import json
import time
import random
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from src.utils import parse_author_data, parse_author_poems, get_proxies
from config.settings import headers_list

proxies = get_proxies()


class AuthorCrawler:
    def __init__(self, base_url, country_code):
        self.base_url = base_url
        self.country_code = country_code

    def fetch_page(self, url):
        for i in range(0, 5):
            headers = random.choice(headers_list)
            pr = random.choice(proxies)
            # headers = {
            #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
            # }
            response = requests.get(url, headers=headers, proxies={'http':pr})
            if response.status_code == 200:
                return response.text
            else:
                # raise ValueError(f"Failed to fetch page from {url}. Status code: {response.status_code}")
                continue
        raise ValueError(f"Failed to fetch page from {url}. Status code: {response.status_code}")


    def crawl_authors_all(self, page_limit=11):
        for i in range(1, page_limit):
            self.crawl_author_page(i)
            time.sleep(10)
        return

    def crawl_author_page(self, page_num):
        page_url = f"{self.base_url}/searchauthor.php?Country={self.country_code}&Sort=Views&SortOrder=desc&Page=&Sort=Views&SortOrder=desc&Page={page_num}"
        html_content = self.fetch_page(page_url)
        print(html_content)
        authors_data = []
        if html_content:
            authors_data = parse_author_data(html_content)
            self.save_authors_link_to_json(authors_data)
        return authors_data

    # def crawl_poems_by_author(self, author_url):
    #     html_content = self.fetch_page(author_url)
    #     if html_content:
    #         return parse_author_poems(html_content)
    #     return []

    def save_authors_link_to_json(self, authors):
        country_code = self.country_code
        # Tạo đường dẫn thư mục nếu chưa có
        data_dir = "data/authors"
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        # Tạo file JSON với tên tương ứng mã quốc gia
        file_path = os.path.join(data_dir, f"country_{country_code}.json")

        # Nếu file đã tồn tại, đọc dữ liệu hiện có
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                existing_data = json.load(file)
        else:
            existing_data = dict()

        # Cập nhật dữ liệu với danh sách các tác giả mới
        existing_data.update(authors)

        # Lưu lại dữ liệu vào file JSON
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(existing_data, file, ensure_ascii=False, indent=4)

        print(f"Saved {len(authors)} authors to {file_path}")