"""scrapping justjoin.it"""
import requests
from bs4 import BeautifulSoup
import csv
import json
from datetime import datetime
import time
import re


class JustJoinScraper:
    def __init__(self):
        self.headers = {
             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",                        
                        }
        self.base_url = "https//justjoin.it"


    def get_page_content(self, url: str) -> str:
        try:
            print(f"Downloading: {url}")
            response = requests.get(url, headers=self.headers)

            if response.status_code == 200:
                return response.text
            else:
                print(f"HTTP error: {response.status_code}")
                None

        except Exception as e:
            print(f"Error while loading page: {e}")
            return None