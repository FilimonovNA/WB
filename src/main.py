from wb_parser import Request, WBParser, Mode
from constants import *
import os
import time
from datetime import datetime
from db_class import PositionsDB

# user = InfoImport()
# info.get_user_request()
# print(info.user_request)
# print(info.get_user_requests_list())
# for request_text in user_requests:
#     for current_page in range(1, 3, 3):
#         r = Request(DEFAULT_ITEM_ID, request_text, current_page).get_request()
#         #d = r.get_data()
#         print(r.request)


def wait():
    print('Ждем 20 сек, т.к. превышено количество запросов')
    for i in range(20):
        print(f'Ждем {i}сек')
        time.sleep(1)


def get_all_requests_positions(item_id, user_requests):
    if isinstance(user_requests, list):
        positions_list = []
        counter = 0
        req_len = len(user_requests)
        for request_text in user_requests:
            counter += 1
            if counter % 10 == 0:
                wait()
            positions_list.append(get_one_request_position(item_id, request_text))
            print(f'{counter}/{req_len}')
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
                return position + (current_page - 1) * MAX_LIMIT

    return None


def clear_terminal():
    # os.system('cls' if os.name == 'nt' else 'clear')
    # print(chr(27) + "[2J")
    # os.system('clear')
    print("\033c\033[3J")


def get_page(position):
    try:
        return int(position / 100) + 1
    except TypeError:
        return None


def mode_1(usr, db):
    print('It\'s mode_1')
    item_id = usr.get_item_id()
    if item_id == 0:
        return 0
    request = usr.get_user_request()
    if request == 0:
        return 0
    position = get_all_requests_positions(item_id, request)
    page = get_page(position)
    date = datetime.now().strftime("%d:%m:%Y")
    row_db = update_dict(date, item_id, request, position)
    print(f'item_id = {item_id}, request = {request}, position = {position}, page = {page}\n')
    db.insert_row(row_db)


def mode_2(usr, db):
    print('It\'s mode_2')
    if isinstance(usr.item_id, int) or isinstance(usr.item_id, str) or usr.item_id is None:
        usr.get_items()
    print(usr.item_id)
    if len(usr.item_id) == 0:
        print('Нет значений в файле Items.txt')
        return 0
    request = usr.get_user_request()
    if request == '0':
        return 0
    positions = {}
    for item in usr.item_id:
        position = get_one_request_position(item, request)
        page = get_page(position)
        positions.update({item: position})
        date = datetime.now().strftime("%d:%m:%Y")
        row_db = update_dict(date, item, request, position)
        print(f'item_id = {item}, request = {request}, position = {position}, page = {page}\n')
        db.insert_row(row_db)


def mode_3(usr, db):
    print('It\'s mode_3')
    item_id = usr.get_item_id()
    if item_id == 1:
        return 0
    requests = usr.get_user_requests_list()
    if requests == 1:
        return 0
    positions = get_all_requests_positions(item_id, requests)
    i = 0
    for position in positions:
        page = get_page(position)
        date = datetime.now().strftime("%d:%m:%Y")
        row_db = update_dict(date, item_id, requests[i], position)
        print(f'request = {requests[i]}, position={position}, page = {page}')
        db.insert_row(row_db)
        i += 1
    save_file(item_id, positions)
    return 0


def mode_4(usr, db):
    print('It\'s mode_4')
    items_id = usr.get_items()
    requests = usr.get_common_requests_list()
    for item in items_id:
        positions = get_all_requests_positions(item, requests)
        i = 0
        for position in positions:
            page = get_page(position)
            date = datetime.now().strftime("%d:%m:%Y")
            row_db = update_dict(date, item, requests[i], position)
            print(f'item_id = {item}, request = {requests[i]}, position={position}, page = {page}')
            db.insert_row(row_db)
            i += 1
        save_file(item, positions)
    return 0


def save_file(file_name, data):
    path = f'responses/{file_name}.txt'
    dt = datetime.now().strftime("%d:%m:%Y %H:%M:%S")
    with open(path, 'w') as file:
        file.write(str(dt)+'\n')
        for one_pos in data:
            page = get_page(one_pos)
            file.write(f'{one_pos}({page})\n')


def update_dict(date, item_ID, request, position):
    if position is None:
        position = 'NULL'
    request = request.replace('+', ' ')
    row_db = {'date': date, 'item_ID': item_ID, 'request': request, 'position': position}
    #row_db.update({'date': date, 'item_ID': item_ID, 'request': request, 'position': position})
    return row_db

def main():
    usr = Mode()
    usr.select_mode()
    db = PositionsDB().create_db()

    while usr.mode != 0:
        if usr.mode == 1:
            mode_1(usr, db)
        elif usr.mode == 2:
            mode_2(usr, db)
        elif usr.mode == 3:
            mode_3(usr, db)
        elif usr.mode == 4:
            mode_4(usr, db)
        usr.select_mode()

    db.commit()
    db.disconnect()


main()
