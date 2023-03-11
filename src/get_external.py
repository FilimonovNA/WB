import os
from constants import *


class InfoImport:

    def __init__(self, item_id=DEFAULT_ITEM_ID, user_request=None, user_requests_list=None):
        self.item_id = item_id
        self.user_request = user_request
        self.user_requests_list = user_requests_list

    def get_user_request(self):
        request = input("Enter user request: ")
        self.user_request = request.replace(" ", "+")
        return self.user_request

    def get_item_id(self):
        self.item_id = input("Enter item id: ")
        try:
            return int(self.item_id)
        except ValueError:
            return 1

    def get_user_requests_list(self):
        path = f'{self.item_id}.txt'
        if not os.path.isfile(path):
            return 1
        self.user_requests_list = []
        with open(path, "r") as file:
            for line in file.readlines():
                self.user_requests_list.append(line.replace(" ", "+").replace("\n", ""))
        if len(self.user_requests_list) > 0:
            return self.user_requests_list
        return 1

