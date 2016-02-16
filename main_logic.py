import requests
from collections import deque
from bs4 import BeautifulSoup
import json


PLATFORMS = ['apache', 'iis', 'nginx', 'lightppd']


queue = deque()
visited_sites = []
histogram = {}

test_print1 = "+++"
test_print2 = "---"
test_print3 = "X X X"


def get_platform(server):
    for pl in PLATFORMS:
        if pl in server.lower():
            return pl
        else:
            return 'Others'


def recursion_on_sites(url):
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, 'html.parser')
    for link in soup.find_all('a'):
        l = link.get('href')
        if type(l) is str:
            if l[-1] is not '/':
                l = l + '/'
            try:
                r1 = requests.get(l, timeout=0.1)
                r1_server = r1.headers['Server']
                if l not in visited_sites:
                    histogram[r1_server] = get_platform(r1_server)

                    visited_sites.append(l)
                    queue.append(r1.url)
                    print(test_print1)
            except:
                try:
                    r1 = requests.get(url + l, timeout=0.1)
                    r1_loc = r1.headers['Location']
                    r1_server = r1.headers['Server']
                    if r1_loc not in visited_sites:
                        histogram[r1_server] = get_platform(r1_server)

                        visited_sites.append(r1_loc)
                        queue.append(r1.url)
                        print(test_print2)
                except:
                    print(test_print3)
                    continue

    try:
        recursion_on_sites(queue.popleft())
    except:
        return

recursion_on_sites('http://register.start.bg/')


with open('servers_histogram.json', 'w') as f:
    json.dump(histogram, f, ensure_ascii=False)
