from django import template

import requests
import geocoder as g
import datetime
from django.conf import settings


KEY = settings.WEATHER_KEY

def get_weather():
    city = g.ip('me').city
    req = requests.get(
        f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={KEY}&units=metric')
    data = req.json()
    city_name = data['name']
    temp = round(int(data['main']['temp']))
    curr_temp = f"{temp} °C"
    date = datetime.datetime.now().strftime("%d-%m-%Y")
    now = datetime.datetime.now()
    day = datetime.datetime.weekday(now)
    days_list = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    week_day = days_list[day]
    icon = f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png"
    return {'city': city_name, 'temp': curr_temp, 'icon': icon, 'date': date, 'day': week_day}


register = template.Library()


@register.inclusion_tag('weather.html')
def show_weather(block_class='weather'):
    weather = get_weather()
    a = {'weather': weather, 'block_class': block_class}
    return a
