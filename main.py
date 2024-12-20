import requests
import json
from bs4 import BeautifulSoup
from os import listdir


if not 'index.html' in listdir():
    open('index.html', 'w').close()

if not 'result.json' in listdir():
    open('result.json', 'w').close()


class Shop:
    def __init__(self):
        self.url = 'https://www.google.com/search?&q='
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; en-US) Gecko/20130401 Firefox/67.4'}

    def correct_text(self, text):
        try: return text.replace('/n', ' ').replace('/t', ' ').replace('/r', ' ').strip()
        except: return 'None'

    def find_price(self, items:list):
        for item in items:
            if '₽' in item.text:
                return item
            
        return '-'


    def search(self, text):
        response = requests.get(self.url + text.replace(' ', '+') + '&tbm=shop', headers=self.headers)
        html = BeautifulSoup(response.content, 'html.parser')

        # with open('index2.html', 'wb') as file:
        #     file.write(response.content)

        items_list = {'search': text, 'items': {}}
        count = 0

        # images = {}

        # requests.text
        

        container = html.find('div', {'class': 'sh-pr__product-results'})
        for item in container.find_all('div', {'class': 'sh-dgr__content'}):
            title = self.correct_text(item.find('h3').text)
            price = self.correct_text(self.find_price(item.find_all('span', {'aria-hidden': "true"})).text)
            link = 'http' + item.find('div', {'class': 'sh-dgr__offer-content'}).find('a').get('href').split('http')[-1].split('?')[0].split('&')[0].split('%')[0]
            img = None
            item_id = None
            try:
                item_id = item.find('img')['id']
                # img = item.find('img')['src']

                img = response.text.split(f"';var _i='{item_id}")[0].split("'")[-1].replace('q\\x3dtbn:', 'q=tbn:').split('\\')[0]
            except: pass


            items_list['items'][count] = {'title': title, 'price': price, 'url': link, 'image': img, 'id': item_id}
            print(title, price, link)
            count += 1

        items_list['count'] = len(items_list['items'])

        with open('result.json', 'w', encoding='utf-8') as save_file:
            json.dump(items_list, save_file, ensure_ascii=False)
            print('File saved!')

if __name__ == '__main__':
    # Shop().search('айфон 16')
    Shop().search(input('Enter search: '))