import requests
from bs4 import BeautifulSoup
import threading
import sys
import time

link_visited_lock = threading.Lock()
results = []

# Standard Python threads don’t have a built-in way to return values, so this custom class handles that
class ReturnValueThread(threading.Thread):  
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result = None

    def run(self):
        if self._target is None:
            return
        try:
            self.result = self._target(*self._args, **self._kwargs)
        except Exception as exc:
            print(f'{type(exc).__name__}: {exc}', file=sys.stderr)

    def join(self, *args, **kwargs):
        super().join(*args, **kwargs)
        return self.result


def crawl(start_page, distance, action, link_visited = set()):
    with link_visited_lock:
        if start_page in link_visited:
            return
        link_visited.add(start_page)

    try:
        response = requests.get(start_page).text
    except:
        print("Could not get the text!")
        return

    result = action(response)
    #yield start_page, result
    results.append((start_page, result))

    if distance <= 0: 
        return
    
    threads = []
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

        threads.append(ReturnValueThread(target = crawl, \
                                       args = (url, distance - 1, action, link_visited)))
        threads[-1].start()
    
    for thread in threads:
        thread.join()
        
    return results

start = time.time()
for url, result in crawl("http://www.ii.uni.wroc.pl", 1, lambda text : 'Python' in text):
    print(f"{url}: {result}")

print(time.time() - start)
