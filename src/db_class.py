import sqlite3
import os


class PositionsDB:

    def __init__(self):
        current_dir = os.getcwd()
        os.chdir('..')
        self.db_path = 'db/positions.db'
        self.connect = sqlite3.connect(self.db_path)
        self.cursor = self.connect.cursor()
        os.chdir(current_dir)

    def create_db(self):
        current_dir = os.getcwd()
        os.chdir('..')
        query = f"""
                CREATE TABLE IF NOT EXISTS Positions
                (
                date TEXT PRIMARY KEY,
                item_ID INTEGER,
                request TEXT,
                item_position INTEGER
                )
                """
        self.cursor.execute(query)
        os.chdir(current_dir)
        return self

    def select_all(self):
        query = f""" SELECT * FROM Positions """
        result = self.cursor.execute(query)
        print(self.cursor.fetchall())
        return result

    def insert_row(self, data_dict: dict):
        query = f""" INSERT INTO Positions (date, item_ID, request, item_position)
                VALUES ('{data_dict.get('date')}', {data_dict.get('item_ID')}, 
                        '{data_dict.get('request')}', {data_dict.get('position')})
                """
        self.cursor.execute(query)

    def disconnect(self):
        self.connect.commit()
        self.connect.close()
