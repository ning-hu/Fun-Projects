import io
import argparse
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from selenium import webdriver

driver = webdriver.Chrome()

def scrape(url, output_file, ch):
    # Fetch the page
    driver.get(url)

    # Wait for the JavaScript to run
    driver.implicitly_wait(10)

    # Parse the page
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Find the div with id "content"
    content_div = soup.find(id="content")

    # Find the direct children of the div
    children = content_div.find_all(recursive=False)

    # Go through each child element of the div
    for child in children:
        if child:
            # Find all the tags to ignore
            tags_to_ignore = child.find_all()
            # Replace the tags with an empty string
            for tag in tags_to_ignore:
                tag.replace_with("")

            # If it's an h2 tag, do something
            if child.name == "h2":
                print(f"{ch}. {child.text}", file=output_file)
            # Otherwise, print the text with a tab and a newline
            elif child.text != "":
                print(f"　　{child.text}", file=output_file)

    # Find the div with id "next"
    next_div = soup.find(id="next")
    # Check if it exists
    if next_div:
        # If it does, get the link and follow it
        next_link = next_div.get("href")
        next_url = urljoin(url, next_link)
        scrape(next_url, output_file, ch+1)

# Parse the command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("url", help="the URL to start scraping from")
parser.add_argument("output_file", help="the file to write the output to")
args = parser.parse_args()

# Open the output file
with io.open(args.output_file, "w", encoding="utf-8") as f:
  # Start the scraper
  scrape(args.url, f, 1)