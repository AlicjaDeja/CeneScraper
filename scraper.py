from bs4 import BeautifulSoup
import requests
import json

url = "https://www.ceneo.pl/45863470#tab=reviews"

response = requests.get(url)

page_dom = BeautifulSoup(response.text, "html.parser")

opinions = page_dom.select("div.js_product-review")

all_opinions = []

while (url):

    response = requests.get(url)
    page_dom = BeautifulSoup(response.text, "html.parser")
    opinions = page_dom.select("div.js_product-review")

    for opinion in opinions:

        opinion_id = opinion["data-entry-id"]
        author = opinion.select_one("span.user-post__author-name").text.strip()
        try:
            rcmd = opinion.select_one("span.user-post__author-recomendation > em").text.strip()
        except AttributeError:
            rcmd = None
        score = opinion.select_one("span.user-post__score-count").text.strip()
        content = opinion.select_one("div.user-post__text").text.strip()
        try:
            posted_on = opinion.select_one("span.user-post__published > time:nth-child(1)")["datetime"]
        except TypeError:
            posted_on = None
        try:
            bought_on = opinion.select_one("span.user-post__published > time:nth-child(2)")["datetime"]
        except TypeError:
            bought_on = None
        useful_for = opinion.select_one("button.vote-yes > span").text.strip()
        useless_for = opinion.select_one("button.vote-no > span").text.strip()
        pros = opinion.select("div.review-feature__title--positives ~ div.review-feature__item")
        pros = [item.text.strip() for item in pros]
        cons = opinion.select("div.review-feature__title--negatives ~ div.review-feature__item")
        cons = [item.text.strip() for item in cons]

        single_opinion = {
            "opinion_id": opinion_id,
            "author": author,
            "rcmd": rcmd,
            "score": score,
            "content": content,
            "posted_on": posted_on,
            "bought_on": bought_on,
            "useful_for": useful_for,
            "useless_for": useless_for,
            "pros": pros,
            "cons": cons
        }
        all_opinions.append(single_opinion)

    try:
        url = "https://www.ceneo.pl"+page_dom.select_one("s.pagination__next")["href"]
    except TypeError:
        url = None

with open("opinions/45863470.json", "w", encoding="UTF-8") as jf:
    json.dump(all_opinions, jf, indent=4, ensure_ascii=False)