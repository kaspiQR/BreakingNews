import requests
from django import template
from django.conf import settings

API_KEY_TWELVE = settings.API_KEY_TWELVE


def get_index():
    req = requests.get(
        f'https://api.twelvedata.com/time_series?symbol=AAPL,VFIAX,AAON,JPM,ZM,TCS&interval=1day&apikey={API_KEY_TWELVE}')
    data = req.json()
    indexes = []
    for key in data.keys():
        name = key
        exchange = data[key]['meta']['exchange']
        closed = round(float(data[key]['values'][0]['close']), 3)
        opened = data[key]['values'][0]['open']
        diff = round(float(opened) - float(closed), 3)
        if diff < 0:
            change_color = 'red'
            icon = '<svg xmlns="http://www.w3.org/2000/svg" width="8" height="6" viewBox="0 0 8 6" fill="none"><path d="M1.1875 1.59375L4 4.40625L6.8125 1.59375" stroke="#F32B19" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
        elif diff > 0:
            change_color = 'green'
            icon = '<svg xmlns="http://www.w3.org/2000/svg" width="8" height="6" viewBox="0 0 8 6" fill="none"><path d="M1.1875 4.40625L4 1.59375L6.8125 4.40625" stroke="#12A560" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
        else:
            change_color = 'gray'
            icon = '<svg xmlns="http://www.w3.org/2000/svg" width="6" height="8" viewBox="0 0 6 8" fill="none"><path d="M1.59375 6.625L4.40625 3.8125L1.59375 1" stroke="#969CB4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'

        indexes.append(
            {'name': name, 'price': closed, 'exchange': exchange, 'diff': diff, 'change_color': change_color,
             'icon': icon}
        )
    return indexes


register = template.Library()


@register.inclusion_tag('nasdaq.html')
def show_index(block_class='indexes'):
    indexes = get_index()
    context = {'indexes': indexes, 'block_class': block_class}
    return context