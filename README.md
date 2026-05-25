# Virtual Economy Analyzer & Web Scraper

A Python script developed to extract, analyze, and track virtual market data from a browser-based platform. This project was created to practice web scraping, session management, and data processing.

## Key Features
* Automated Data Extraction: Uses `requests` and `BeautifulSoup4` to navigate and parse paginated HTML tables.
* Session Handling: Implements HTTP POST requests for user authentication and access to protected routes.
* State Tracking: Utilizes local JSON files to store historical market data and detect new transactions.
* Basic Data Analysis: Calculates cross-currency exchange ratios to identify profitable in-game investment opportunities.
* Accessible Output: Generates simple text-based reports optimized for screen readers (e.g., NVDA).

## Technologies Used
* Python 3
* BeautifulSoup4
* Requests
* Regular Expressions (re)
* JSON

## Setup and Usage
1. Clone the repository:
   `git clone https://github.com/blr0708/Virtual-Economy-Analyzer.git`

2. Install the required dependencies:
   `pip install -r requirements.txt`

3. Update credentials:
   Open the script and replace `YOUR_EMAIL` and `YOUR_PASSWORD` in the `login_data` dictionary with the appropriate login details.

4. Run the script:
   `python main.py`
   *(Note: Replace main.py with the actual filename if it differs).*

## Project Purpose
This script was developed as a personal educational project to demonstrate practical skills in Python automation, working with HTTP requests, and structuring unstructured web data.
