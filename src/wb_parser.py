from constants import *
import requests
from get_external import InfoImport
import time


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
        return None


class WBParser:

    def __init__(self, item_id, data):
        self.item_id = item_id
        self.data = data

    def get_position(self):
        position = 0
        for data in self.data['data']['products']:
            position += 1
            if data['id'] == self.item_id:
                return position
        return -1


class Mode(InfoImport):

    def __init__(self):
        super().__init__()
        self.request = None
        self.position = None
        self.page = None

    def mode_1(self):
        print('It\'s mode_1')
        self.item_id = self.get_item_id()
        if self.item_id == 0:
            return 0
        self.request = self.get_user_request()
        if self.request == 0:
            return 0
        self.position = self.get_all_requests_positions()
        self.page = self.get_page()
        print(f'item_id = {self.item_id}, request = {self.request}, position = {self.position}, page = {self.page}\n')

    def get_one_request_position(self, request_text):
        for current_page in range(1, MAX_PAGE):
            request = Request(self.item_id, request_text, current_page).get_request()
            response = request.get_data()
            if response is not None:
                position = WBParser(self.item_id, response).get_position()
                print(position)
                if position != -1:
                    return position + (current_page - 1) * MAX_LIMIT
        return None

    def get_all_requests_positions(self):
        if isinstance(self.request, list):
            positions_list = []
            counter = 0
            req_len = len(self.request)
            for request_text in self.request:
                counter += 1
                if counter % 10 == 0:
                    self.wait()
                positions_list.append(self.get_one_request_position(request_text))
                print(f'{counter}/{req_len}')
            return positions_list
        else:
            self.position = self.get_one_request_position(self.request)
            return self.position

    @staticmethod
    def wait():
        print('Ждем 20 сек, т.к. превышено количество запросов')
        for i in range(20):
            print(f'Ждем {i}сек')
            time.sleep(1)

    def get_page(self):
        try:
            return int(self.position / 100) + 1
        except TypeError:
            return None
