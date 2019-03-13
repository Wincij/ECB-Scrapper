from django.shortcuts import render
from rates.models import Rate
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


def getRate(link):
    """ This function reads content from RSS and scrap it to get currency rate info. It returns string like '0.86145 GBP = 1 EUR 2019-03-12 ECB Reference rate'  """
    request = requests.get(link)
    html = request.content.decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    #The most up-to-date rate at 0 index. So we will be intrested only in this one
    lastRate = soup.find_all('item')[0]


    return lastRate.title.get_text()


def home(request):
    context = {}
    links = getLinks()
    for link in links:
        # 1.9558 BGN = 1 EUR 2019-03-12 ECB Reference rate <- this is simple output of getRate(), we need currency rate and currency name, so we split the output
        splited = getRate(link).split()
        key = splited[1]
        context[key] = float(splited[0])
        rate = Rate(currency = key, cost = context[key])
        rate.save()
    #After we created dictonairy of up-to-date currency rates we can parse it to our render function.

    return render(request, 'home.html', {"context": context})
