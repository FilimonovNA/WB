import sqlite3
import os


class PositionsDB:

    def __init__(self):
        self.db_path = 'db/positions.db'
        self.connect = sqlite3.connect(self.db_path)
        self.cursor = self.connect.cursor()

    def create_db(self):
        query = f"""
                CREATE TABLE IF NOT EXISTS Positions
                (
                id INTEGER PRIMARY KEY,
                date TEXT,
                item_ID INTEGER,
                request TEXT,
                item_position INTEGER
                )
                """
        self.cursor.execute(query)
        return self

    def select_all(self):
        query = f""" SELECT * FROM Positions """
        result = self.cursor.execute(query)
        print(self.cursor.fetchall())
        return result

    def insert_row(self, data_dict: dict):
        query = f""" INSERT OR REPLACE INTO Positions (date, item_ID, request, item_position)
                VALUES ('{data_dict.get('date')}', {data_dict.get('item_ID')}, 
                        '{data_dict.get('request')}', {data_dict.get('position')})
                """
        self.cursor.execute(query)

    def commit(self):
        self.connect.commit()

    def disconnect(self):
        self.connect.close()
