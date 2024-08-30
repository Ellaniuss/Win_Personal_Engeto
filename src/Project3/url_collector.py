import requests
from bs4 import BeautifulSoup as bs


def collect_urls(main_url):
    '''
    Extracts and filters URLs from given webpage withe specified pattern (link has to contain "ps311?"),
    and returns list of absolute urls.

    :param main_url:
        URL used to create soup and scrape links.
    :return: list
        List containing absolute URLs that contains "ps32?x".
    '''
    response = requests.get(main_url)
    base_url = "https://volby.cz/pls/ps2017nss/"

    soup = bs(response.content, 'html.parser')

    relative_url = soup.find_all('a', href=True)

    urls = set()

    for url in relative_url:
        if url['href'].startswith('ps311?'):
            full_url = base_url + url['href']
            urls.add(full_url)

    return urls

url = "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=1&xnumnuts=1100"
links = collect_urls(url)



