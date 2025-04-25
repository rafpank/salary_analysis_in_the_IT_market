# IT Market Salary Analysis

## Project Overview

This repository contains the **project plan** and initial setup for a data science tool aimed at analyzing IT job market salaries based on job offers from platforms such as [NoFluffJobs](https://nofluffjobs.com/pl), RocketJobs, and LinkedIn. 

The goal of this project is to help employers understand the current salary landscape by collecting and analyzing job offer data, including required skills, technologies, locations (including remote options), and to provide data-driven recommendations on competitive salary offers that attract talent without overpaying.

> **Note:** This is an ongoing project planned to be developed over the coming months. The repository will be regularly updated with new features, data pipelines, and analysis tools.

## Key Features (Planned)

- **Automated web scraping** of job offers with respect to site policies and ethical scraping practices.
- **Data normalization** using NLP techniques to unify job titles, skills, and technologies across different listings.
- **Salary prediction models** that consider:
  - Required skills and technologies
  - Location and remote work options
  - Historical salary trends
- **Interactive visualizations** using Matplotlib and Plotly for easier data exploration.
- **Filtering capabilities** by skills, job titles, and locations to handle varying naming conventions.
- **Recommendation engine** for optimal salary offers and employee benefits (a “nice-to-have” feature).
- **Automated adaptation** of scrapers to handle changes in website structures.

## Data Storage Approach

Initially, raw scraped data may be stored in CSV files for simplicity and ease of use on a local machine. However, as the project grows, a NoSQL database like MongoDB might be introduced for better handling of semi-structured data and scalability.

## Technologies (Planned)

- Python 3.9+
- Web scraping: Scrapy, BeautifulSoup, Selenium (if needed)
- NLP: spaCy
- Data processing: pandas, NumPy
- Machine Learning: scikit-learn
- Visualization: Matplotlib, Plotly
- Data storage: CSV / MongoDB
- Task automation: Airflow / Cron (optional)
- Testing: pytest

## Getting Started

### Clone the repository

git clone https://github.com/rafpank/salary_analysis_in_the_IT_market.git
cd salary_analysis_in_the_IT_market

