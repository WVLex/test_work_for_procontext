import datetime

import lxml.html
import requests
import statistics




x = 0
dictionary = dict()
for i in range(5):
    date = datetime.datetime.now() - datetime.timedelta(days=x)
    actual_date = datetime.datetime.strftime(date, '%d/%m/%Y')
    x += 1

    r = requests.get(f'http://www.cbr.ru/scripts/XML_daily_eng.asp?date_req={actual_date}')
    tree = lxml.html.fromstring(r.text.encode())


    for currency in tree.getchildren():
        temp_data = {}
        for data in currency.getchildren():
            if data.tag == 'name':
                temp_data[data.text] = 0
            elif data.tag == 'value':
                value = float('.'.join(data.text.split(',')))
                temp_data[list(temp_data.keys())[0]] = {actual_date: value}
        try:
            dictionary[list(temp_data.keys())[0]] += [temp_data[list(temp_data.keys())[0]]]
        except KeyError:
            dictionary[list(temp_data.keys())[0]] = []
            dictionary[list(temp_data.keys())[0]] += [temp_data[list(temp_data.keys())[0]]]


# Самая дорогая валюта
all_values = []
for currency in list(dictionary.items()):
    for current_value in currency[1]:
        all_values += list(current_value.values())
mx = max(all_values)
full_name_max = None
for i in dictionary:
    for x in dictionary[i]:
        if mx in list(x.values()):
            full_name_max = i + ' ' + str(mx) + ' ' + list(x.keys())[0]
print('Самая дорогая валюта')
print(full_name_max, '\n')


# Самая дешёвая валюта
all_values = []
for currency in list(dictionary.items()):
    for current_value in currency[1]:
        all_values += list(current_value.values())
mx = min(all_values)
full_name_min = None
for currency in dictionary:
    for current_value in dictionary[currency]:
        if mx in list(current_value.values()):
            full_name_min = currency + ' ' + str(mx) + ' ' + list(x.keys())[0]


print('Самая дешёвая валюта')
print(full_name_min, '\n')


# Среднее

all_prices = dict()
for currency in dictionary:
    cur_mean = []
    for current_value in dictionary[currency]:
        cur_mean += list(current_value.values())
    all_prices[currency] = statistics.mean(cur_mean)

print('Среднее:')
for i in all_prices:
    print(i + ':', round(all_prices[i], 3))

