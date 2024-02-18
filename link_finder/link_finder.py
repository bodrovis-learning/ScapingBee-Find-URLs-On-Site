import requests
from bs4 import BeautifulSoup as Soup
import os
import csv

# from scrapingbee import ScrapingBeeClient

# Constants for the attributes to be extracted from the sitemap.
ATTRS = ["loc", "lastmod", "priority"]


def parse_sitemap(url):
    """Parse the sitemap at the given URL and append the data to a CSV file."""
    # Return False if the URL is not provided.
    if not url:
        return False

    # Attempt to get the content from the URL.
    response = requests.get(url)
    # Return False if the response status code is not 200 (OK).
    if response.status_code != 200:
        return False

    # ALTERNATIVELY, use ScrapingBee!
    # from scrapingbee import ScrapingBeeClient

    # client = ScrapingBeeClient(
    #     api_key="YOUR_API_KEY"
    # )
    # response = client.get(
    #     url,
    #     params={
    #         # Enable proxy:
    #         # 'premium_proxy': 'true',
    #         # 'country_code': 'gb',
    #         "block_resources": "false",
    #         "wait": "1500" # Waiting for the content to load (1.5 seconds)
    #         # Make screenshot if needed:
    #         # "screenshot": True,
    #         # "screenshot_full_page": True,
    #     }
    # )

    # Parse the XML content of the response.
    soup = Soup(response.content, "xml")

    # Recursively parse nested sitemaps.
    for sitemap in soup.find_all("sitemap"):
        loc = sitemap.find("loc").text
        parse_sitemap(loc)

    # Define the root directory for saving the CSV file.
    root = os.path.dirname(os.path.abspath(__file__))

    # Find all URL entries in the sitemap.
    urls = soup.find_all("url")

    rows = []
    for url in urls:
        row = []
        for attr in ATTRS:
            found_attr = url.find(attr)
            # Use "n/a" if the attribute is not found, otherwise get its text.
            row.append(found_attr.text if found_attr else "n/a")
        rows.append(row)

    # Append the data to the CSV file.
    with open(os.path.join(root, "data.csv"), "a+", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)


# Example usage
parse_sitemap("https://bodrovis.tech/sitemap.xml")
