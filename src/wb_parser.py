from constants import *
import requests


class Request:

    def __init__(self, item_id, request_text, page):
        self.item_id = item_id
        self.request_text = request_text
        self.page = page
        self.request = 'None'

    def get_request(self):
        self.request = f'https://search.wb.ru/exactmatch/ru/female/v4/search?appType=1&couponsGeo=2,12,3,18,15,21' \
                  f'&curr=rub&dest=123585734&emp=0&lang=ru&locale=ru&pricemarginCoeff=2.0&' \
                  f'query={self.request_text}&page={self.page}&limit={MAX_LIMIT}&' \
                  f'reg=1&regions=80,64,38,4,115,83,33,68,70,69,30,86,75,40,1,66,31,48,110,22,71' \
                  f'&resultset=catalog&sort=popular&spp=50&sppFixGeo=4&suppressSpellcheck=false'
        return self

    def get_data(self):
        response = requests.get(self.request, headers=HEADER)
        if response.status_code == 200:
            data = response.json()
            if len(data) == 5:
                return data
            else:
                return None


class WBParser:

    def __init__(self, item_id, data):
        self.item_id = item_id
        self.data = data

    def get_position(self, item_id=DEFAULT_ITEM_ID):
        position = 0
        for data in self.data['data']['products']:
            position += 1
            if data['id'] == item_id:
                return position
        return -1

