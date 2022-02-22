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
        """Загрузка информации из бд по ключу key.
        Возвращает список [name, nickname, password, icon] \n
        login - нужная талица в БД \n
        key - ключ, по каторому нужно загрузить информацию"""
               
        self.cursor.execute('SELECT * FROM {}'.format(login))
        rows = self.cursor.fetchall()

        for note in rows:
            if note[0] == key:
                return list(map(str, note))

    def load_all_name(self, login: str) -> list:
        """Возвращает все записи из таблицы нужной таблицы. \n
        login - нужная таблица в БД \n"""

        self.cursor.execute('SELECT * FROM {}'.format(login))
        rows = self.cursor.fetchall()
        return [note[0] for note in rows]

    def save(self, login: str, arr: list):
        """Сохранение списка arr [name, nickname, password, icon].
        Каждый эдлемент соответственно в свое поле БД. \n
        login - нужная табдица в БД \n
        arr - сохраняемый список"""
        
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
        """Создание новой таблицы в БД \n
        login - название новой таблицы"""

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
                self.connection.commit()
                self.save(login, ["Example", "test2020@gmail.com", "123456789", "default"])
            except sqlite3.OperationalError:
                pass

        else:
            self.connect_db()
            self.create_new_table(login)


    def delete_note(self, login: str, key: str):
        """Удаление строчки по заначению key в стобце name из таблицы login в БД. \n
        login - нужная табkbwf в БД \n
        key - значение в ячейке name (ключ по котрой будет удалена строчка)"""

        self.cursor.execute("DELETE FROM {0} WHERE {1} = '{2}'".format(login, "name", key))
        self.connection.commit()


class DB_hash:

    def __init__(self):
        if os.path.isdir('sources'): 
            "Если в данной дирректории есть папка sources"

            if "hashedpasswords.db" not in os.listdir("sources"):
                file = open("sources\\hashedpasswords.db", "w+")
                file.close()
        else:
            os.mkdir("sources")
            file = open("sources\\hashedpasswords.db", "w+")
            file.close()
        self.connect_db()
        self.check_table()

    def connect_db(self):
        "Подключение к БД"

        self.connection = sqlite3.connect("sources\\hashedpasswords.db", check_same_thread=False)
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

    def saving(self, login: str, key: bytes, salt: bytes):
        """Cохраняет ключ и соль для пользоваетля \n
        login - нужный пользователь \n
        key - сохраняемый ключ \n
        salt - сохраняемая соль"""

        info_cells = list(self.cursor.execute("PRAGMA table_info(hash);"))
        keys =[]
        for i in info_cells:
            keys.append(i[1])
        keys = ", ".join(keys)

        vaules = f"\"{login}\", \"{str(key)}\", \"{str(salt)}\""
        
        operation = (f'INSERT or REPLACE into hash ({keys}) VALUES ({vaules})')
        self.cursor.execute(operation)
        self.connection.commit()

    def load(self, login: str) -> tuple or None:
        """Возвращает (key, salt) из БД. Если записи не существует возвращает None \n
        login - нужный пользователь, по котрому нужно загрузить кортеж"""

        self.cursor.execute('SELECT * FROM hash')
        rows = self.cursor.fetchall()
        if rows is None:
            return None
        for note in rows:
            if note[0] == login:
                return tuple(map(str, note[1:]))

    def create_new_table(self):
        """Создание таблицы в БД (в случае ее отсутствия)"""

        if self.check_connection():

            len_cells = 3
            name_of_cells = ['login', 'key', 'salt']
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
                self.cursor.execute(f'CREATE TABLE hash({cells})')
            except sqlite3.OperationalError:
                pass

            self.connection.commit()

    def check_table(self):
        """Проверка существования таблицы. В случае отсутвия создает ее."""

        try:
            self.cursor.execute('SELECT * FROM hash')
        except sqlite3.OperationalError:
            self.create_new_table()
    

    def delete_note(self, login: str):
        """Удаление входных данных пользователя в БД. \n
        login - нужный пользователь"""

        self.cursor.execute("DELETE FROM {0} WHERE {1} = '{2}'".format('hash', 'name', login))
        self.connection.commit()


if __name__ == "__main__":
    test = DB()
    test.create_new_table("tokar")
    test.save("tokar", ["steam", "kek", "123", "+"])
    print(test.load("tokar", "steam"))
    print(test.load_all_name('tokar'))

    test2 = DB_hash()
    test2.saving("tokar", bytes('10101100', encoding='utf-8'), bytes('100110110', encoding='utf-8'))
    print(test2.load('tokar'))