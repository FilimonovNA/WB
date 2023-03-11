from constants import *
import requests


class WBParser:

    def __init__(self, item_id, requests_list, last_page):
        self.item_id = item_id
        self.requests_list = requests_list
        self.last_page = last_page


class Request:

    def __init__(self, item_id, request_text, page):
        self.item_id = item_id
        self.request_text = request_text
        self.page = page
        self.request = 'None'

    def get_request(self):
        self.request = f'https://search.wb.ru/exactmatch/ru/female/v4/search?appType=1&couponsGeo=2,12,3,18,15,21' \
                  f'&curr=rub&dest=123585734&emp=0&lang=ru&locale=ru&pricemarginCoeff=2.0&' \
                  f'query={self.request_text}&page={self.page}&limit=300&' \
                  f'reg=1&regions=80,64,38,4,115,83,33,68,70,69,30,86,75,40,1,66,31,48,110,22,71' \
                  f'&resultset=catalog&sort=popular&spp=50&sppFixGeo=4&suppressSpellcheck=false'
        return self

    def get_data(self):
        response = requests.get(self.request, headers=HEADER)
        data = response.json()
        # data_list = get_data_from_json_request(data)
        return data
