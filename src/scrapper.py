from bs4 import BeautifulSoup
from selectors import selectors
from utils import get_html_by_url, write_links_to_file
from urllib.parse import urlparse, parse_qsl
from datetime import datetime

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 ' \
                  'Safari/537.36 '
}


def get_and_write_sellers(url):
    parsed_url = urlparse(url)
    domain_page = f'{parsed_url.scheme}://{parsed_url.netloc}'
    asin = get_asin(parsed_url)
    sellers_page_link = get_sellers_link(url, domain_page)
    products_sellers_links = get_new_product_sellers_links(sellers_page_link, domain_page, asin)
    filename = f'links_{datetime.now()}.txt'
    write_links_to_file(filename, 'Sellers of new products', products_sellers_links)
    return filename


def get_sellers_link(url, domain):
    product_page = get_html_by_url(url, headers)
    soup = BeautifulSoup(product_page, 'lxml')
    link = soup.select_one(selectors['sellers_page'])
    href = link.get('href')
    return f'{domain}{href}'


def get_product_sellers_links(sellers_page_link, domain, asin, next_page_selector, sellers_links_selector):
    sellers_page = get_html_by_url(sellers_page_link, headers)
    soup = BeautifulSoup(sellers_page, 'lxml')
    next_page = soup.select_one(next_page_selector)
    sellers_ids = map(lambda a: get_seller_by_href(a.get('href')), soup.select(sellers_links_selector))
    sellers_links = list(map(lambda id: form_seller_link_by_id(domain, asin, id), sellers_ids))
    if next_page is not None:
        next_page_link = f'{domain}/{next_page.get("href")}'
        return sellers_links + get_product_sellers_links(next_page_link,
                                                         domain,
                                                         asin,
                                                         next_page_selector,
                                                         sellers_links_selector)
    return sellers_links


def get_new_product_sellers_links(sellers_page_link, domain, asin):
    return get_product_sellers_links(sellers_page_link,
                                     domain,
                                     asin,
                                     selectors['new_sellers_next_page'],
                                     selectors['new_sellers_links'])


def form_seller_link_by_id(domain, asin, seller_id):
    return f'{domain}/dp/{asin}?m={seller_id}'


def get_seller_by_href(href):
    query = urlparse(href).query
    seller_id = dict(parse_qsl(query))['seller']
    return seller_id


def get_asin(parsed_url):
    splitted_path = parsed_url.path.split('/')
    return splitted_path[3]
