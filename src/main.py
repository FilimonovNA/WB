from get_external import InfoImport
from wb_parser import Request, WBParser
from constants import *
import os


#user = InfoImport()
# info.get_user_request()
# print(info.user_request)
# print(info.get_user_requests_list())
# for request_text in user_requests:
#     for current_page in range(1, 3, 3):
#         r = Request(DEFAULT_ITEM_ID, request_text, current_page).get_request()
#         #d = r.get_data()
#         print(r.request)


def get_all_requests_positions(item_id, user_requests):
    if isinstance(user_requests, list):
        positions_list = []
        for request_text in user_requests:
            positions_list.append(get_one_request_position(item_id, request_text))
        return positions_list
    else:
        return get_one_request_position(item_id, user_requests)


def get_one_request_position(item_id, request_text):
    for current_page in range(1, MAX_PAGE):
        request = Request(item_id, request_text, current_page).get_request()
        response = request.get_data()
        if response is not None:
            position = WBParser(request.item_id, response).get_position()
            if position != -1:
                return position + (current_page-1) * MAX_LIMIT

    return None


def clear_terminal():
   # os.system('cls' if os.name == 'nt' else 'clear')
   # print(chr(27) + "[2J")
   # os.system('clear')
    print("\033c\033[3J")


def mode_1(usr):
    clear_terminal()
    print('It\'s mode_1')
    item_id = usr.get_item_id()
    if item_id == 0:
        return 0
    request = usr.get_user_request()
    if request == 0:
        return 0
    position = get_all_requests_positions(item_id, request)
    try:
        page = int(position)
    except TypeError:
        page = None
    print(f'item_id = {item_id}, request = {request}, position = {position}, page = {page}\n')


def mode_2():
    print('It\'s mode_2')


def mode_3():
    print('It\'s mode_3')


def mode_4():
    print('It\'s mode_4')


def main():
    usr = InfoImport()
    usr.select_mode()
    while usr.mode != 0:
        if usr.mode == 1:
            mode_1(usr)
        elif usr.mode == 2:
            mode_2()
        elif usr.mode == 3:
            mode_3()
        elif usr.mode == 4:
            mode_4()
        usr.select_mode()


main()
