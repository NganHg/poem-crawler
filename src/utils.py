from bs4 import BeautifulSoup
import requests

def parse_author_data(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    authors = dict()
    
    for author in soup.find_all('h4', class_='list-item-header'):
        author_link = author.find('a').get('href')
        author_name = author.text
        authors[author_name] = author_link
    
    return authors

def parse_author_poems(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    poem_groups = soup.find_all('div', class_='poem-group-list')

    # Danh sách để lưu các link
    links = []

    # Duyệt qua từng div và lấy các link trong đó
    for group in poem_groups:
        # Tìm tất cả các thẻ <a> trong div
        anchors = group.find_all('a')
        for a in anchors:
            link = a['href']  # Lấy giá trị của thuộc tính href
            links.append(link)
    
    return links

def parse_poem_data(html_content):
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        # print(soup)
        title = soup.find('header', class_='page-header').find('h1').text
        content = soup.find('div', class_='poem-content').get_text(separator='\n', strip=True)
        # author = soup.find('a', class_='author-link').text
        info = soup.find('div', class_='summary-section').find_all('a')
        poem_form = info[0].text
        period = info[1].text
    except:
        return None

    return {
        'Title': title,
        'Content': content,
        # 'author': author
        'Poem Form': poem_form,
        'Period': period
    }

def get_proxies():
    url = "https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=protocolipport&format=text"
    
    try:
        # Gửi yêu cầu đến API
        response = requests.get(url)
        
        # Kiểm tra nếu yêu cầu thành công
        if response.status_code == 200:
            proxies = response.text.splitlines()
            
            # Lọc các proxy bắt đầu bằng 'http'
            http_proxies = [proxy for proxy in proxies if proxy.startswith("http")]
            
            return http_proxies
        else:
            print(f"Failed to fetch proxies. Status code: {response.status_code}")
            return []
    
    except requests.RequestException as e:
        print(f"An error occurred while fetching proxies: {e}")
        return []