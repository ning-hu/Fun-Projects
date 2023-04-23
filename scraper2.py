import io
import argparse
import requests
from bs4 import BeautifulSoup

def scrape(url, output_file):
    # Fetch the page
    response = requests.get(url)

    # Parse the page
    soup = BeautifulSoup(response.text, "html.parser")

    title_div = soup.find(id="nr_title")
    if title_div:
        print(f"{title_div.text}", file=output_file)

    # Find the div with id "nr1
    content_div = soup.find(id="nr1")

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

            if ("e" in child.text or "E" in child.text or child.text == ""):
                continue
            
            print(f"　　{child.text}", file=output_file)

    # Find the li with class "next"
    next_li = soup.find("li", class_="next")
    # Check if it exists
    if next_li:
        # If it does, get the link and follow it
        next_a = next_li.find("a")
        if next_a:
            next_link = next_a.get("href")
            scrape(next_link, output_file)

# Parse the command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("url", help="the URL to start scraping from")
parser.add_argument("output_file", help="the file to write the output to")
args = parser.parse_args()

# Open the output file
with io.open(args.output_file, "w", encoding="utf-8") as f:
  # Start the scraper
  scrape(args.url, f)