import os
import sqlite3

class DB:
    def __init__(self):
        if os.path.isdir('sources'): 
            "Если в данной дирректории есть папка sources"

            if "data.db" not in os.listdir("sources"):
                file = open("sources\\data.db", "w+")
                file.close()
        else:
            os.mkdir("sources")
            file = open("sources\\data.db", "w+")
            file.close()
        self.connect_db()

    def connect_db(self):
        "Подключение к БД"
        self.connection = sqlite3.connect("sources\\data.db", check_same_thread=False)
        self.cursor = self.connection.cursor()

    def connection_close(self):
        "Отключение от БД"
        if self.cursor is not None:
            self.cursor.close()
        if self.connection is not None:
            self.connection.close()
    
    def check_connection(self) -> bool:
        "Проверка соединения"
        if self.cursor is not None:
            if self.connection is not None:
                return True

    def load(self, login: str, key: str) -> list:
        """Загрузка информации из бд по ключу.
        Возвращает список [name, nickname, password, icon]
        login - нужная талица в БД."""
               
        self.cursor.execute('SELECT * FROM {}'.format(login))
        rows = self.cursor.fetchall()

        for note in rows:
            if note[0] == key:
                return list(map(str, note))

    def save(self, login: str, arr: list):
        """Сохранение списка arr [name, nickname, password, icon].
        Каждый эдлемент соответственно в свое поле БД.
        login - нужная табдица в БД"""
        
        info_cells = list(self.cursor.execute("PRAGMA table_info({});".format(login)))
        keys =[]
        for i in info_cells:
            keys.append(i[1])
        keys = ", ".join(keys)

        string = lambda x: "'" + x + "'"
        vaules = ', '.join(list(map(string, arr)))
        
        operation = (f'INSERT or REPLACE into {login} ({keys}) VALUES ({vaules})')
        self.cursor.execute(operation)
        self.connection.commit()

    def create_new_table(self, login: str):
        """Создание новой таблицы в БД"""
        if self.check_connection():

            len_cells = 4
            name_of_cells = ['name', 'nickname', 'password', 'icon']
            key = 0
            cells = ''

            for i in range(len_cells):
                if key == i:
                    cell = f'{name_of_cells[i]} string PRIMARY KEY, '
                else:
                    cell = f'{name_of_cells[i]} string, '
                cells += cell
            cells = cells.rstrip(cells[-1])
            cells = cells.rstrip(cells[-1])
            try:
                self.cursor.execute(f'CREATE TABLE {login}({cells})')
            except sqlite3.OperationalError:
                pass

            self.connection.commit()

if __name__ == "__main__":
    test = DB()
    test.create_new_table("tokar")
    test.save("tokar", ["steam", "kek", "123", "+"])
    print(test.load("tokar", "steam"))