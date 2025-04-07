import requests
from bs4 import BeautifulSoup
import time


def crawl(start_page, distance, action, link_visited = set()):
    if start_page in link_visited: 
        return
    
    link_visited.add(start_page)

    try:
        response = requests.get(start_page).text
    except:
        print("Could not get the text!")
        return

    result = action(response)
    yield (start_page, result)

    if distance <= 0: 
        return

    soup = BeautifulSoup(response, 'html.parser')
    for link in soup.find_all('a'):
        url = link.get('href')

        if url is None: 
            continue
        
        is_new_url = url.startswith('http') or url.startswith('https')

        if is_new_url and "ii." not in url: 
            continue

        if not(is_new_url):
            url = start_page + url

        yield from crawl(url, distance - 1, action, link_visited)


start = time.time()
for url, result in crawl("http://www.ii.uni.wroc.pl", 2, lambda text : 'Python' in text):
    print(f"{url}: {result}")

print(time.time() - start)