from django.shortcuts import render

# Create your views here.
from bs4 import BeautifulSoup
import requests



"""
    First we use reuquests to get every currency RSS from https://www.ecb.europa.eu/home/html/rss.en.html.
    We use BeautifulSoup to get all content. We will use this link list later
"""

def getLinks():
    """ This function returns complete list of necessary RSS channels from official ECB website"""
    page = 'https://www.ecb.europa.eu/home/html/rss.en.html'
    request = requests.get(page)
    html = request.content.decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    currencies = soup.find_all('a', class_="rss")
    link_list = []
    for currency in currencies:
        # Some RSS's are for other purposes than getting currencies rates. All used for currencies contains fxref in href
        if 'fxref' in currency['href']:
            link_list.append("https://www.ecb.europa.eu" + currency['href'])

    # We crated completed list of RSS
    return link_list
