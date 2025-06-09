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
        

    def parse_offer_card(self, offer_element: str):
        """
        Parses a single offer card from HTML
        """
        try:
            offer_data = {}

            link_element = offer_element
            if link_element.name == 'a' and link_element.get('href'):
                relative_link = link_element.get('href')
                offer_data['link'] = f"{self.base_url}{relative_link}"
                offer_data['slug'] = relative_link.replace('/job-offer/','')
            else:
                offer_data['link'] = 'Ther are no links'
                offer_data["slug"] = ''

            # Job Title in h3
            title_element = offer_element.find('h3', class_ = 'css=1gehlh0')
            offer_data['title'] = title_element.get_text(strip=True) if title_element else 'No title'


            # Company  - in span (building icon)
            company_element = offer_element.find('svg', {'data-testid': 'ApartmentRoundedIcon'})
            if company_element:
                company_span = company_element.find_next('span')
                offer_data['company'] = company_span.get_text(strip=True) if company_span else 'No company name'
            else:
                offer_data['company'] = 'No company name'

            # Location - in span with location icon
            location_element = offer_element.find('svg', {'data-testid': 'PlaceOutlinedIcon'})
            if location_element:
                location_container = location_element.find_next('div', class_='css-vc0lhh')
                if location_container: 
                    location_span = location_container.find('span', class_='css=1o4wo1x')
                    offer_data['location'] = location_span.get_text(strip=True) if location_span else 'No location'
                else:
                    offer_data['location'] = 'No location'
            else:
                offer_data['location'] = 'No location'

            # Work mode (remte/office)
            remote_element = offer_element.find('span', class_='css-1uevhcf')
            if remote_element:
                offer_data['workplace_type'] = remote_element.get_text(strip=True)
            else:
                # Checking if is "Fully remote" badge
                remote_tag = offer_element.find('div', string='Fully remote')
                offer_data['workplace_type'] = 'Fully remote' if remote_tag else 'Office'

            # Salary 
            salary_container = offer_element.find('div', class_='css-18ypp16')
            if salary_container:
                salary_spans = salary_container.find_all('span')
                if len(salary_spans) <= 3:
                    # First span - amount from, second span - amount to, third span - currency/period
                    salary_from = salary_spans[0].get_text(strip=True)
                    salary_to = salary_spans[1].get_text(strip=True)
                    currency_period = salary_spans[2].get_text(strip=True)
                    offer_data['salary_info'] = f"{salary_from} - {salary_to} {currency_period}"
                else:
                    offer_data['salary_info'] = salary_container.get_text(strip=True)
            else:
                offer_data['salary_info'] = 'No information about salary'

            # Skills in skill tags
            skills = []
            skill_tags = offer_element.find_all('div', class_=re.compile(r'skill-tag-\d+'))
            for skill_tag in skill_tags:
                skill_div = skill_tag.find('div', class_='css-jikuwi')
                if skill_div:
                    skills.append(skill_div.get_text(strip=True))

            offer_data['reuired_skills'] = skills

            # Is this a new offer
            new_tag = offer_element.find('div', class_='css-jikuwi', string='New')
            offer_data['is_new'] = bool(new_tag)

            # Company logo
            logo_img = offer_element.find('img', id='offerCardCompanyLogo')
            offer_data['company_logo'] = logo_img.get('src') if logo_img else ''

            return offer_data
        

        except Exception as e:
            print(f"Error while parsing the offer: {e}")
            return None
