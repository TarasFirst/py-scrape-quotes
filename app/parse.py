import csv
import requests
from dataclasses import dataclass, astuple, fields

from bs4 import BeautifulSoup, Tag

BASE_URL = "https://quotes.toscrape.com/"


@dataclass
class Quote:
    text: str
    author: str
    tags: list[str]


QUOTES_FIELDS =[field.name for field in fields(Quote)]


def write_fields_name_csv(output_csv_path: str) -> None:
    with open(output_csv_path, "a", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(QUOTES_FIELDS)


def parse_single_quote(quote: Tag) -> Quote:
    return Quote(
        text=quote.select_one(".text").text,
        author=quote.select_one(".author").text,
        tags=[tag.text for tag in quote.select(".tag")],
    )

def get_soup(url: str=BASE_URL) -> BeautifulSoup:
    text = requests.get(url).content
    return BeautifulSoup(text, features="html.parser")


def get_single_page_quotes(url: str=BASE_URL) -> [Quote]:
    soup = get_soup(url)
    all_quotes = soup.select(".quote")
    return [parse_single_quote(quote) for quote in all_quotes]


def write_csv(output_csv_path: str, url) -> None:
    quotes = get_single_page_quotes(url)
    with open(output_csv_path, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows([astuple(quote) for quote in quotes])


def parse_all_site(output_csv_path: str):
    write_fields_name_csv(output_csv_path)
    all_quotes = get_single_page_quotes()
    num_page = 1
    soup = get_soup()
    while soup.select_one(".next"):
        url = f"{BASE_URL}/page/{num_page}"
        write_csv(output_csv_path, url)
        num_page += 1
        soup = get_soup(f"{BASE_URL}/page/{num_page}")
    return all_quotes


def main(output_csv_path: str) -> None:
    return parse_all_site(output_csv_path)


if __name__ == "__main__":
    main("quotes.csv")
