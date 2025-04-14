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

BASE_URL = "https://www.straitstimes.com"

def get_forum_links():
    # Setup headless Chrome browser
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(f"{BASE_URL}/opinion/forum")

    # Wait for dynamic content to load
    time.sleep(3)

    # Find article link elements
    elements = driver.find_elements(By.CSS_SELECTOR, "a[data-testid='subsection-card-wrapper']")
    print(f"Found {len(elements)} links with subsection-card-wrapper")

    links = []
    for el in elements:
        href = el.get_attribute("href")
        if href and "/opinion/forum/" in href:
            links.append(href)

    driver.quit()
    return links

import json

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