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
            title_element = offer_element.find('h3', class_ = 'css-1gehlh0')
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
        

    def scrape_job_offers(self, location="slask", max_pages = 5):
        all_offers = []

        for page in range(1, max_pages + 1):
            if page == 1:
                url = f"{self.base_url}/job-offers/{location}"
            else:
                url = f"{self.base_url}/job-offers/{location}?page={page}"

            html_content = self.get_page_content(url)
            if not html_content:
                print(f"Failed to download page {page}")
                break

            soup = BeautifulSoup(html_content, 'html.parser')

            # Finding all of offer cards
            offer_cards =soup.find_all('a', class_='offer-card')

            if not offer_cards:
                print(f"No offer found on the site {page}")
                print("I'm checking alternative selectors...")

                alternative_selectors = [
                    'a[href*="/job-offer/"]',
                    '[data-testid="offer-card"]',
                    '.job-offer-card',
                    'div[class*="offer"]'
                ]

                for selector in alternative_selectors:
                    offer_cards = soup.select(selector)
                    if offer_cards:
                        print(f"Found {len(offer_cards)} offers using selector: {selector}")
                        break

                if not offer_cards:
                    # Chceckin if the page loaded correctly
                    if 'justjoin' in html_content.lower():
                        print("The justjoin.it page loaded but no offers has been found")
                        print("Display part of HTML")
                        print(html_content[:1000])
                    break

            print(f"{len(offer_cards)} has been found on page {page}")

            # Parsing all of offers
            page_offers = []
            for card in offer_cards:
                offer = self.parse_offer_card(card)
                if offer:
                    page_offers.append(offer)
                    all_offers.append(offer)

            print(f"Successfully parsed {len(page_offers)} offesrs from {page}")

            if len(offer_cards) == 0:
                break

            # Delay between requests
            time.sleep(2)

        return all_offers
    

    def save_to_csv(self, offers, filename=None):
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"justjoin_offers_{timestamp}.csv"

        
        if not offers:
            print("There is no offers to be recorded")
            return
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = [
                    'title', 'company', 'location', 'workplace_type', 
                    'salary_info', 'required_skills', 'is_new', 'link', 'slug'
                ]

                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                for offer in offers:
                    csv_offer = offer.copy()
                    csv_offer['required_skills'] = ', '.join(offer.get('required_skills', []))

                    writer.writerow(csv_offer)

            print(f"Saved{len(offers)} offers to the file: {filename}")
            return filename
        
        except Exception as e:
            print(f"An error occurred while saving to CSV: {e}")
            return None
        

    def save_to_json(self, offers, filename=None):
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"justjoin_offers_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(offers, f, ensure_ascii=False, indent=2)
            print(f"Full data has been saved to file: {filename}")
            return filename
        except Exception as e:
            print(f"An error occurred while saving to JSON: {e}")
            return None
        

    def print_offers_summary(self, offers):
        if not offers: 
            print("Ther is no offers to display")
            return
        
        print(f"\n=== Summary of: {len(offers)} offers ===")

        # Displays the first 10 offers

        for i, offer in enumerate(offers[:10], 1):
            print(f"\n{i}. {offer['title']}")
            print(f"   Company: {offer['company']}")
            print(f"   Location: {offer['location']}")
            print(f"   Work mode: {offer['workplace_type']}")
            print(f"   Salary: {offer['salary_info']}")
            print(f"   Skills: {', '.join(offer.get('required_skills', []))}")
            print(f"   Link: {offer['link']}")

        if len(offers) > 10:
            print(f"\n... and {len(offers) - 10} more offers")

    def debug_page_structure(self, url):
        html_content = self.get_page_content(url)
        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')


            print("=== DEBUGGING THE WEBSITE STRUCTURE ===")
            print(f"Website title: {soup.title.string if soup.title else 'There is no title'}")

            # Check various possible selectors
            selectors_to_check = [
                ('a.offer-card', 'Links with class offer_card'),
                ('a[href*="/job-offer/"]', 'Links containing /job-offer/'),
                ('h3', 'All h3 elements'),
                ('[class*="offer"]', 'Elements with "offer" in class'),
                ('[class*="job"]', 'Elements with "job" in class'),
                ('[class*="card"]', 'Elements with "card" in class'),
            ]
            
            for selector, description in selectors_to_check:
                elements = soup.select(selector)
                print(f"{description}: {len(elements)} elements")

                if elements and len(elements) <= 3:
                    for i, elem in enumerate(elements[:3]):
                        print(f"  {i+1}. {elem.name} - {elem.get('class', [])} - {elem.get_text(strip=True)[:100]}...")


def main():
    scrpaper = JustJoinScraper()

    # Checking structure of website
    print("=== DEBUGGING PAGE STRUCTURE ===")
    test_url = "http://justjoin.it/job-offers/slask"
    scrpaper.debug_page_structure(test_url)

    print("\n" + "="*50)
    print("=== START DOWNLOADING OFFERS ===")
    
    offers = scrpaper.scrape_job_offers(location='slask', max_pages=3)

    if offers:
        # Display page summary
        scrpaper.print_offers_summary(offers)

        # saving to the files
        csv_file = scrpaper.save_to_csv(offers)
        json_file = scrpaper.save_to_json(offers)
                