import csv
import logging
# import sys
import requests
from dataclasses import dataclass, astuple, fields

from bs4 import BeautifulSoup, Tag

BASE_URL = "https://quotes.toscrape.com/"


@dataclass
class Quote:
    text: str
    author: str
    tags: list[str]


# QUOTES_FIELDS =[field.name for field in fields(Quote)]


def parse_single_quote(quote: Tag) -> Quote:
    return Quote(
        text=quote.select_one(".text").text,
        author=quote.select_one(".author").text,
        tags=[tag.text for tag in quote.select(".tag")],
    )


def get_all_quotes() -> [Quote]:
    text = requests.get(BASE_URL).content
    soup = BeautifulSoup(text, features="html.parser")
    all_quotes = soup.select(".quote")
    print ([parse_single_quote(quote) for quote in all_quotes])



# def get_single_page_quotes(page_soup: Tag) -> [Quote]:
#     quotes = page_soup.select(".text")
#     return [parse_single_quote(quote) for quote in quotes]
#
#
# def get_url_current_page():
#     return
#
#
#     # href = "/page/1/"
#
#     current_page = f"{BASE_URL}page/{num_page}"
#
#     while BeautifulSoup(requests.get(BASE_URL).content).select_one(".next"):
#         all_quotes.extend(get_single_page_quotes(next_page_soup))
#     return all_quotes
#
#
# def write_csv(quotes: [Quote]) -> None:
#     with open("output_csv_path", "w") as csvfile:
#         writer = csv.writer(csvfile)
#         writer.writerow(QUOTES_FIELDS)
#         writer.writerows([astuple(quote) for quote in quotes])
#
# QUOTES = get_all_quotes()


# def main(output_csv_path: str) -> None:
#     with open(output_csv_path, "w") as csvfile:
#         writer = csv.writer(csvfile)
#         writer.writerow(QUOTES_FIELDS)
#         writer.writerows([astuple(quote) for quote in QUOTES])

def main():
    # return get_all_quotes()
    get_all_quotes()

if __name__ == "__main__":
    # main("quotes.csv")
   main()
