import requests
from bs4 import BeautifulSoup
import pandas as pd

data = {'flat_name': [], 'society_name': [], 'rate': [], 'Carpet Area': [],
        'Status': [], 'Floor': [], 'Transaction': [], 'Furnishing': [],
        'Facing': [], 'Overlooking': [], 'Society': [], 'Ownership': [],
        'Bathroom': [], 'Balcony': []}

base_url = 'https://www.magicbricks.com/flats-in-pune-for-sale-pppfs'

pages_to_scrap = 350

page = 1

while page <= pages_to_scrap:
    url = f'{base_url}/page-{page}'
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')

    flats = soup.find_all('div', class_='mb-srp__list')

    if not flats:
        break

    for flat in flats:
        flat_name = flat.find('h2', class_='mb-srp__card--title').text
        society_name = flat.find('a', class_='mb-srp__card__society--name')
        details = flat.find_all('div', class_='mb-srp__card__summary__list--item')
        rate = flat.find('div', class_='mb-srp__card__price--amount')

        details_dict = {}
        for detail in details:
            label = detail.find('div', class_='mb-srp__card__summary--label').text
            value = detail.find('div', class_='mb-srp__card__summary--value').text
            details_dict[label] = value

        data['flat_name'].append(flat_name)
        data['society_name'].append(society_name.text if society_name else 'Not specified')
        data['rate'].append(rate.text)
        data['Carpet Area'].append(details_dict.get('Carpet Area', 'Not specified'))
        data['Status'].append(details_dict.get('Status', 'Not specified'))
        data['Floor'].append(details_dict.get('Floor', 'Not specified'))
        data['Transaction'].append(details_dict.get('Transaction', 'Not specified'))
        data['Furnishing'].append(details_dict.get('Furnishing', 'Not specified'))
        data['Facing'].append(details_dict.get('facing', 'Not specified'))
        data['Overlooking'].append(details_dict.get('overlooking', 'Not specified'))
        data['Society'].append(details_dict.get('Society', 'Not specified'))
        data['Ownership'].append(details_dict.get('Ownership', 'Not specified'))
        data['Bathroom'].append(details_dict.get('Bathroom', 'Not specified'))
        data['Balcony'].append(details_dict.get('Balcony', 'Not specified'))

    page += 1

df = pd.DataFrame(data)

print(df)
print("Number of pages scrapped: ", page)

df.to_excel('Flats_data_Pune_v1.xlsx', index=False);


