from bs4 import BeautifulSoup
import requests
import json

def get_element(parent, selector, attribute = None, return_list=False):
    try:
        if return_list:
            return [item.text.strip() for item in parent.select(selector)]
        if attribute:
            return parent.select_one(selector)[attribute]
        return opinion.select_one("span.user-post__author-recomendation > em").text.strip()
    except (AttributeError, TypeError):
        return None

product_id = input("Please enter the product id: ")

url = f"https://www.ceneo.pl/{product_id}#tab=reviews"

response = requests.get(url)

page_dom = BeautifulSoup(response.text, "html.parser")

opinions = page_dom.select("div.js_product-review")

all_opinions = []

while (url):

    response = requests.get(url)
    page_dom = BeautifulSoup(response.text, "html.parser")
    opinions = page_dom.select("div.js_product-review")

    for opinion in opinions:

        single_opinion = {
            "opinion_id": opinion["data-entry-id"],
            "author": get_element(opinion, "span.user-post__author-name"),
            "rcmd": get_element(opinion, "span.user-post__author-recomendation > em"),
            "score": get_element(opinion, "span.user-post__score-count"),
            "content": get_element(opinion, "div.user-post__text"),
            "posted_on": get_element(opinion, "span.user-post__published > time:nth-child(1)","datetime"),
            "bought_on": get_element(opinion, "span.user-post__published > time:nth-child(2)", "datetime"),
            "useful_for": get_element(opinion, "button.vote-yes > span"),
            "useless_for": get_element(opinion, "button.vote-no > span"),
            "pros": get_element(opinion, "div.review-feature__title--positives ~ div.review-feature__item", None, True),
            "cons": get_element(opinion, "div.review-feature__title--negatives ~ div.review-feature__item", None, True)
        }
        all_opinions.append(single_opinion)

    try:
        url = "https://www.ceneo.pl"+page_dom.select_one("s.pagination__next")["href"]
    except TypeError:
        url = None

with open(f"opinions/{product_id}.json", "w", encoding="UTF-8") as jf:
    json.dump(all_opinions, jf, indent=4, ensure_ascii=False)