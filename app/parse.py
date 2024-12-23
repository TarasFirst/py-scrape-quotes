import csv
import time
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


def get_soup(url: str, session: requests.Session) -> BeautifulSoup:
    response = session.get(url)
    return BeautifulSoup(response.content, features="html.parser")


def get_single_page_quotes(soup: BeautifulSoup) -> [Quote]:
    all_quotes = soup.select(".quote")
    return [parse_single_quote(quote) for quote in all_quotes]


def write_csv(output_csv_path: str, quotes: [Quote]) -> None:
    with open(output_csv_path, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows([astuple(quote) for quote in quotes])


def parse_all_site(output_csv_path: str):
    write_fields_name_csv(output_csv_path)
    session = requests.Session()
    num_page = 1
    while True:
        url = f"{BASE_URL}/page/{num_page}"
        soup = get_soup(url, session)
        quotes = get_single_page_quotes(soup)
        if not quotes:
            break
        write_csv(output_csv_path, quotes)
        print(f"Processed page {num_page}")
        num_page += 1
        time.sleep(1)


def main(output_csv_path: str) -> None:
    return parse_all_site(output_csv_path)


if __name__ == "__main__":
    main("quotes.csv")
