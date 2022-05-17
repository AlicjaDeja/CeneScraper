from translate import Translator
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

opinion_elements ={
            "author": ["span.user-post__author-name"],
            "rcmd": ["span.user-post__author-recomendation > em"],
            "score": ["span.user-post__score-count"],
            "content": ["div.user-post__text"],
            "posted_on": ["span.user-post__published > time:nth-child(1)","datetime"],
            "bought_on": ["span.user-post__published > time:nth-child(2)", "datetime"],
            "useful_for": ["button.vote-yes > span"],
            "useless_for": ["button.vote-no > span"],
            "pros": ["div.review-feature__title--positives ~ div.review-feature__item", None, True],
            "cons": ["div.review-feature__title--negatives ~ div.review-feature__item", None, True]
        }

to_lang = "en"
from_lang = "pl"
translator = Translator(to_lang=to_lang, from_lang=from_lang)

product_id = input("Please enter the product id: ")
url = f"https://www.ceneo.pl/{product_id}#tab=reviews"

all_opinions = []

while (url):
    print(url)
    response = requests.get(url)
    page_dom = BeautifulSoup(response.text, "html.parser")
    opinions = page_dom.select("div.js_product-review")

    for opinion in opinions:

        single_opinion = {
            key: get_element(opinion, *values)
            for key, values in opinion_elements.items()
        }

        single_opinion["opinion_id"] = opinion["data-entry-id"]
        single_opinion["rcmd"] = True if single_opinion["rcmd"] == "Polecam" else False if single_opinion["rcmd"] == "Nie polecam" else None
        single_opinion["score"] = float(single_opinion["score"].split("/")[0].replace(",","."))
        single_opinion['useful_for'] = int(single_opinion["useful_for"])
        single_opinion["useless_for"] = int(single_opinion["useless_for"])
        single_opinion["content_en"] = translator.translate(single_opinion["content"])
        all_opinions.append(single_opinion)

    try:
        url = "https://www.ceneo.pl"+page_dom.select_one("s.pagination__next")["href"]
    except TypeError:
        url = None

with open(f"opinions/{product_id}.json", "w", encoding="UTF-8") as jf:
    json.dump(all_opinions, jf, indent=4, ensure_ascii=False)