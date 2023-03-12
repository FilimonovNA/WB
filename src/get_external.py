import os


class InfoImport:

    def __init__(self):
        self.mode = 1
        self.item_id = None
        self.user_request = None
        self.user_requests_list = None

    def select_mode(self):
        mode = -1
        while 0 > mode or mode > 4:
            print('Выберите режим работы:\n'
                  '0 - Выход из программы\n'
                  '1 - Одиночный запрос для одного артикула\n'
                  '2 - Одиночный запрос для нескольких артикулов\n'
                  '3 - Множественный запрос для одного артикула\n'
                  '4 - Множественный запрос для нескольких артикулов\n')
            mode = input('Введите цифру от 0 до 4:  ')
            try:
                mode = int(mode)
            except ValueError:
                mode = -1
                print('Это не цифра\n')
        self.mode = mode
        return self

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

    def get_items(self):
        self.item_id = []
        current_dir = os.getcwd()
        os.chdir('..')  # поднимаемся на одну ступень выше
        path = f'user_requests/items.txt'
        if not os.path.isfile(path):
            os.chdir(current_dir)
            return 1
        with open(path, "r") as file:
            self.item_id = [x for x in file.readlines()]

        os.chdir(current_dir)
        items = []
        for item in self.item_id:
            try:
                items.append(int(item))
            except ValueError:
                pass

        self.item_id = items
        return self.item_id

    def get_user_requests_list(self):
        current_dir = os.getcwd()
        os.chdir('..')  # поднимаемся на одну ступень выше
        path = f'user_requests/{self.item_id}.txt'
        if not os.path.isfile(path):
            os.chdir(current_dir)
            return 1
        self.user_requests_list = []
        with open(path, "r") as file:
            for line in file.readlines():
                self.user_requests_list.append(line.replace(" ", "+").replace("\n", ""))
        os.chdir(current_dir)
        if len(self.user_requests_list) > 0:
            return self.user_requests_list
        return 1

    def get_common_requests_list(self):
        current_dir = os.getcwd()
        os.chdir('..')  # поднимаемся на одну ступень выше
        path = f'user_requests/common.txt'
        if not os.path.isfile(path):
            os.chdir(current_dir)
            return 1
        self.user_requests_list = []
        with open(path, "r") as file:
            for line in file.readlines():
                self.user_requests_list.append(line.replace(" ", "+").replace("\n", ""))
        os.chdir(current_dir)
        if len(self.user_requests_list) > 0:
            return self.user_requests_list
        return 1
