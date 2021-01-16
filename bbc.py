#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import requests
from bs4 import BeautifulSoup

def get_bbc_headline():
    url = 'https://www.bbc.co.uk/news'
    r = requests.get(url)
    html_doc = r.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    topstories = soup.find(id='nw-c-topstories-england')
    headline = topstories.h3.get_text()
    primer = topstories.p.get_text()
    return headline, primer

if __name__ == "__main__":
    headline, primer = get_bbc_headline()
    print("BBC News")
    print("--------")
    print("Headline: {}".format(headline))
    print(primer)
    print()
