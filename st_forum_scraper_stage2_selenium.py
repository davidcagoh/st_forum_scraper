"""
Straits Times Forum Scraper - Stage 2 (Content Extraction)
---------------------------------------------------------
This script uses Selenium to visit each forum article, extract the title,
date, and body text, and then save the data to a CSV file.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import csv
from st_forum_scraper_stage1_selenium import main as get_forum_links
import json

BASE_URL = "https://www.straitstimes.com"

def load_forum_links():
    try:
        with open("forum_links.json", "r") as file:
            forum_links = json.load(file)
        print(f"Loaded {len(forum_links)} forum links.")
        return forum_links
    except FileNotFoundError:
        print("forum_links.json not found.")
        return []

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_article_details(url):
    # Setup headless Chrome browser
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    # Wait until article content is fully loaded
    try:
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".article-content"))
        )

        # Extract article title, date, and body text
        title = driver.find_element(By.CSS_SELECTOR, "h1").text
        date = driver.find_element(By.CSS_SELECTOR, "button.updated-timestamp").text
        body = driver.find_element(By.CSS_SELECTOR, ".article-content").text

        return {
            "title": title,
            "date": date,
            "body": body
        }

    except Exception as e:
        print(f"Failed to extract article: {url}\nReason: {e}")
        return None

    finally:
        driver.quit()

def save_to_csv(articles):
    # Save extracted article data to a CSV file
    with open("forum_articles.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["title", "date", "body"])
        writer.writeheader()
        for article in articles:
            writer.writerow(article)


def main():
    # Get forum links from Stage 1
    forum_links = load_forum_links()  # Corrected function call to Stage 1's main()
    articles = []
    total_articles = len(forum_links)

    for i, url in enumerate(forum_links, start=1):
        print(f"Scraping article {i} of {total_articles}: {url}")
        article_details = get_article_details(url)
        if article_details:
            articles.append(article_details)
            print(f"Extracted: {article_details['title']}")
        else:
            print(f"Failed to extract article from {url}")
        
        # Show progress percentage
        progress = (i / total_articles) * 100
        print(f"Progress: {i}/{total_articles} ({progress:.2f}%)")

    # Save the data to CSV
    save_to_csv(articles)
    print(f"Saved {len(articles)} articles to forum_articles.csv.")


if __name__ == "__main__":
    main()