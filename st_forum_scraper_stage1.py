import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.straitstimes.com"
FORUM_URL = f"{BASE_URL}/opinion/forum"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
}

def get_forum_links():
    response = requests.get(FORUM_URL, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch page: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    links = []
    
    print(f"Found {len(soup.select("a[data-testid='subsection-card-wrapper']"))} links with subsection-card-wrapper")

    for article in soup.select("a[data-testid='subsection-card-wrapper']"):
        href = article.get("href")
        if href and "/opinion/forum/" in href:
            full_url = BASE_URL + href
            links.append(full_url)

    return links

if __name__ == "__main__":
    forum_links = get_forum_links()
    print(f"Found {len(forum_links)} forum links:")
    for link in forum_links:
        print(link)