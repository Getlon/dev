TOKEN = ''

keys = {
    'рубль': 'RUB',
    'доллар': 'USD',
    'евро': 'EUR'
}

currencies = ''
count = 0
for key in keys:
    count += 1
    if count == len(keys):
        currencies += key + '.'
    else:
        currencies += key + ', '
