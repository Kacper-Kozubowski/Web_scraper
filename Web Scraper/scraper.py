import string
import os

import requests
from http import HTTPStatus
from bs4 import BeautifulSoup


pages = int(input("How many pages to search: "))
article_type = input("What type of article do you want: ")

for page in range(1, pages + 1):

    url = f"https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&year=2020&page={page}"
    response = requests.get(url)

    if response.status_code != HTTPStatus.OK:
        print(f"The URL returned {response.status_code}")
        exit(1)

    os.makedirs(f"Page_{page}", exist_ok=True)

    soup = BeautifulSoup(response.content, "html.parser")
    articles = soup.find_all("article")
    news_articles = []
    for article in articles:
        article_span = article.find("span", {"data-test": "article.type"})
        if article_span and article_span.text == article_type:
            news_articles.append(article)

    news_articles_contents = []
    for article in news_articles:
        a = article.find("a", {"data-track-action": "view article"})
        article_link = "https://www.nature.com/nature" + a["href"]

        article_response = requests.get(article_link)
        if article_response.status_code != HTTPStatus.OK:
            print(f"The URL returned {article_response.status_code}")
            continue

        article_soup = BeautifulSoup(article_response.content, "html.parser")
        content = article_soup.find("p", {"class": "article__teaser"}).text
        title = article_soup.find("head").find("title").text

        title = "".join(char for char in title if char not in string.punctuation)
        title = title.strip().replace(" ", "_").replace("\n", "")

        file = open(f"Page_{page}/{title}.txt", "w", encoding="utf-8")
        file.write(content)
        file.close()

    print("Content saved")
