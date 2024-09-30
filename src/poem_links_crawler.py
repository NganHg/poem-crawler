import os
import json
import time
import random
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from src.utils import get_proxies, parse_author_poems
from config.settings import headers_list

proxies = get_proxies()

class PoemLinkCrawler:
    def __init__(self, base_url):
        self.base_url = base_url

    def fetch_page(self, url):
        for i in range(5):
            headers = random.choice(headers_list)
            pr = random.choice(proxies)
            response = requests.get(url, headers=headers, proxies={'http': pr})
            if response.status_code == 200:
                return response.text
            else:
                continue
        raise ValueError(f"Failed to fetch page from {url}. Status code: {response.status_code}")

    def crawl_poem_all(self):
        with open('data/authors/country_2.json', 'r', encoding='utf-8') as file:
            authors_data = json.load(file)
        try:
            with open('data/poems/poems_links.json', 'r', encoding='utf-8') as file:
                authors_data_completed = json.load(file)
        except:
            authors_data_completed = dict()

        authors_data = {k: v for k, v in authors_data.items() if k not in authors_data_completed}

        for author, url in authors_data.items():
            self.crawl_poem_page(url, author)
            time.sleep(10)  # Dừng 10 giây giữa các yêu cầu

    def crawl_poem_page(self, author_url, author_name):
        full_url = f"{self.base_url}{author_url}"
        html_content = self.fetch_page(full_url)
        if html_content:
            poems_data = parse_author_poems(html_content)
            self.save_poems_to_json(poems_data, author_name)

    def save_poems_to_json(self, poems, author_name):
      data_dir = "data/poems"
      if not os.path.exists(data_dir):
          os.makedirs(data_dir)

      file_path = os.path.join(data_dir, "poems_links.json")

      # Nếu file đã tồn tại, đọc dữ liệu hiện có
      if os.path.exists(file_path):
          with open(file_path, 'r', encoding='utf-8') as file:
              existing_data = json.load(file)
      else:
          existing_data = {}

      # Cập nhật dữ liệu với danh sách các liên kết bài thơ mới
      existing_data[author_name] = existing_data.get(author_name, []) + poems

      # Lưu lại dữ liệu vào file JSON
      with open(file_path, 'w', encoding='utf-8') as file:
          json.dump(existing_data, file, ensure_ascii=False, indent=4)

      print(f"Saved {len(poems)} poems links for author '{author_name}' to {file_path}")

# Khởi tạo và chạy crawler
if __name__ == "__main__":
    base_url = "http://your_base_url_here"  # Thay thế bằng URL cơ sở của bạn
    crawler = PoemLinkCrawler(base_url)
    crawler.crawl_poem_all()