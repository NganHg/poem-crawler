import requests
import os
import time
import random
import json
from src.utils import parse_poem_data, get_proxies
from config.settings import headers_list

proxies = get_proxies()

class PoemCrawler:
    def __init__(self, base_url):
        self.base_url = base_url

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

    def crawl_poem(self, poem_url, author_name):
        full_url = f"{self.base_url}{poem_url}"
        html_content = self.fetch_page(full_url)
        if html_content:
            poems_data = parse_poem_data(html_content)
            if poems_data is None:
                return
            poems_data["Author"] = author_name
            poems_data["Link"] = full_url
            self.save_poems_to_json(poems_data)

    def crawl_poem_all(self, poem_num=10):
        with open('data/poems/poems_links.json', 'r', encoding='utf-8') as file:
            author_poem_links = json.load(file)

        for author, urls in author_poem_links.items():
            for url in urls[:poem_num]:
                self.crawl_poem(url, author)
                time.sleep(10)  # Dừng 10 giây giữa các yêu cầu

    def save_poems_to_json(self, poem):
      data_dir = "data/poems"
      if not os.path.exists(data_dir):
          os.makedirs(data_dir)

      file_path = os.path.join(data_dir, "poems.json")

      # Nếu file đã tồn tại, đọc dữ liệu hiện có
      if os.path.exists(file_path):
          with open(file_path, 'r', encoding='utf-8') as file:
              existing_data = json.load(file)
      else:
          existing_data = []

      # Cập nhật dữ liệu với danh sách các liên kết bài thơ mới
      existing_data.append(poem)

      # Lưu lại dữ liệu vào file JSON
      with open(file_path, 'w', encoding='utf-8') as file:
          json.dump(existing_data, file, ensure_ascii=False, indent=4)

      print(f"Saved {poem.get('Title')} as {len(existing_data)}th poem")

