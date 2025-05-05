"scrapping justjoin.it"
import requests
from bs4 import BeautifulSoup

HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Accept-Language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7"
    }

# URL = 'https://nofluffjobs.com/pl/slask'
START_URL = 'https://justjoin.it/job-offers/slask'


def get_offer_links(page_url):
    response = requests.get(page_url, headers=HEADERS)


def page_dowlanding(url: str):
    response = requests.get(url, headers=HEADERS)
    return response

def main():
    print(page_dowlanding(START_URL))


if __name__ == '__main__':
    main()