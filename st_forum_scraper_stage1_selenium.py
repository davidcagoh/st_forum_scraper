"""
Straits Times Forum Scraper - Stage 1 (Selenium)
------------------------------------------------
This script uses Selenium to render the dynamically loaded Forum page,
extracts all article links using their data-testid attribute,
and prints the URLs. Meant for headless usage and further expansion.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

BASE_URL = "https://www.straitstimes.com"
MAX_ARTICLES = 50  # We'll stop scraping once this many links are collected

def get_forum_links():
    # Setup headless Chrome browser
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(f"{BASE_URL}/opinion/forum")

    links = []  # Keep this list to collect links across pages

    while len(links) < MAX_ARTICLES:
        # Wait for dynamic content to load
        time.sleep(3)

        print("Current page URL:", driver.current_url)

        # Find article link elements
        elements = driver.find_elements(By.CSS_SELECTOR, "a[data-testid='subsection-card-wrapper']")
        print(f"Found {len(elements)} links with subsection-card-wrapper")

        for el in elements:
            href = el.get_attribute("href")
            if href and "/opinion/forum/" in href:
                links.append(href)
            if len(links) >= MAX_ARTICLES:
                break

        if len(links) >= MAX_ARTICLES:
            break

        # Approach 1: Try clicking the "Next" button 
        next_button = driver.find_elements(By.CSS_SELECTOR, "a.page-next")
        if next_button:
            print("Found next page button. Clicking...")
            next_href = next_button[0].get_attribute("href")
            print("Next page URL:", next_href)
            driver.get(next_href)  # Navigate to the next page

        else:
            print("No next page button found.")
            break  # Exit loop if no next page

        # Approach 2: Manually hardcode the next page URL

    driver.quit()
    return links

def main():
    forum_links = get_forum_links()
    if not forum_links:
        print("No forum links found!")
        return []
    
    # Save links to a JSON file
    with open("forum_links.json", "w") as file:
        json.dump(forum_links, file, indent=2)

    print(f"Collected and saved {len(forum_links)} forum links.")
    return forum_links

if __name__ == "__main__":
    main()