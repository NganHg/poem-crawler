# Poem Crawler

A Python-based web scraper designed to collect author information, poem links, and poem content from [Thivien.net](https://www.thivien.net). The collected data is processed and can be indexed into Elasticsearch.

## Dependencies

This project relies on the following key libraries:

*   **requests**: For handling HTTP requests and managing proxy/user-agent rotation.
*   **beautifulsoup4**: For parsing HTML content and extracting relevant data.
*   **elasticsearch**: For interfacing with an Elasticsearch cluster to store the crawled poems.

## Installation

1.  Clone the repository:
    ```bash
    git clone <repository-url>
    cd poem-crawler
    ```

2.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3.  (Optional) Configure your environment settings in `config/settings.py` (e.g., Elasticsearch host, target URLs).

## Usage

```bash
python main.py
```