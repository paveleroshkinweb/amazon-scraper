import requests
import time
from fp.fp import FreeProxy
from requests import ConnectionError
from itertools import cycle
import os


proxy_list = cycle(FreeProxy().get_proxy_list())


def get_html_by_url(url, headers=None):
    for proxy in proxy_list:
        try:
            response = requests.get(url, headers=headers, proxies={'http': proxy})
            if response.ok:
                return response.text
        except ConnectionError:
            time.sleep(.5)
            return get_html_by_url(url, headers)


def write_links_to_file(filename, header, links):
    path_to_file = f'{os.getcwd()}/links/{filename}'
    mode = 'a' if os.path.exists(path_to_file) else 'w'
    with open(path_to_file, mode) as file:
        file.write(header + '\n')
        file.write('\n'.join(links) + '\n')
