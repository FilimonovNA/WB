from get_external import InfoImport
from wb_parser import Request
from constants import *

info = InfoImport()
# info.get_user_request()
# print(info.user_request)
# print(info.get_user_requests_list())

request_text = info.get_user_request()
for current_page in range(1, 3, 3):
    r = Request(DEFAULT_ITEM_ID, request_text, current_page).get_request()
    #d = r.get_data()
    print(r.request)
