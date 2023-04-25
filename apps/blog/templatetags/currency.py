from django import template
from django.conf import settings

import requests
from bs4 import BeautifulSoup


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0',
    "accept": "text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8"
}
URL = settings.URL_CAPITAL


def get_html(URL, headers=HEADERS, params=' '):
    html = requests.get(URL, headers=headers, params=params).text
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def get_data(soup):
    data = []
    items = soup.find('div', class_='summary').find('table', class_='summary-currencies').find('tbody').find_all('tr')
    for item in items:
        try:
            print(f'{item} \n')
            symbol = item.find('td', class_='table-symbol').text
            price = item.find('td', class_='table-price').find('span').text
            price_change_icon = item.find('img').get('src')
            price_change_icon_src = f"{URL}{price_change_icon}"
            price_change = item.find('span', class_='price-change').text
            print(float(price_change))
            if float(price_change) < 0:
                change_color = 'red'
            elif float(price_change) == 0:
                change_color = 'gray'
            else:
                change_color = 'green'
        except:
            symbol = None
            price = None
            price_change_icon = None
            price_change = None
            change_color = None
        if symbol is not None:
            data.append({
                'symbol': symbol,
                'price': price,
                'price_change_icon_src': price_change_icon_src,
                'price_change': price_change,
                'change_color': change_color
            })
    return data


def get_common_info(items):
    data = []
    curr_column = items.find('div', class_='summary-table--data').find_all('div', class_='summary-table--column')
    for col in curr_column:
        try:
            pair = col.find('h6').text
            price = col.find('h5').text
            price_change_icon = col.find('h5').find('img').get('src')
            price_change_icon_src = f"{URL}{price_change_icon}"
            price_change = col.find('span', class_='price-change').text
            if float(price_change) < 0:
                change_color = 'red'
            elif float(price_change) == 0:
                change_color = 'gray'
            else:
                change_color = 'green'
        except:
            pair = None,
            price = None,
            price_change_icon = None,
            price_change_icon_src = None,
            price_change = None,
            change_color = None
        data.append({
            'pair': pair,
            'price': price,
            'price_change_icon_src': price_change_icon_src,
            'price_change': price_change,
            'change_color': change_color
        })

    return data


soup = get_html(URL)
register = template.Library()


@register.inclusion_tag('currency.html')
def show_currency(block_class='currency-wrapper'):
    currency = get_data(soup)
    items_tables = soup.find_all('div', class_='summary-table')
    crypto_data = get_common_info(items_tables[0])
    petrol_data = get_common_info(items_tables[1])
    metal_data = get_common_info(items_tables[2])
    a = {'currency': currency, 'petrol_data': petrol_data, 'metal_data': metal_data, 'crypto_data': crypto_data,
         'block_class': block_class}
    return a
