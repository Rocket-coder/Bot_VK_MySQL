import sqlite3 as sql


#Вся работа с SQLite3


#Внесение нового пользователя в таблицу

def insert(id, name, _class):
    try:
        con = sql.connect('test.db')
        cur = con.cursor()
        print("............\nЗапрос к SQLite по импорту...\n")
        cur.execute("CREATE TABLE IF NOT EXISTS 'users' ('_id' INTEGER,"
                    "                                   '_name' STRING, "
                    "                                   '_class' STRING,"
                    "                                   '_status' INTEGER        "
                    ")")

        sqllite_select = f"""SELECT _id FROM users WHERE _id = {id}"""
        sqllite_ins = f"""INSERT INTO 'users' VALUES ('{id}', '{name}', '{_class}', '0')"""
        cur.execute(sqllite_select)

        #Проверка на наличие пользователя в БД
        if cur.fetchone() is None:
            cur.execute(sqllite_ins)
            con.commit()
            print(f'Пользователь {id} добавлен')
        else:
            print('Пользователь есть в БД!')
            cur.close()
            return

        cur.close()
    except sql.Error as error:
        print("###Ошибка при работе с SQLite:", error)
    finally:
        if con:
            con.close()
            print("\nСоединение с SQLite закрыто.\n............")

#
def new_or_old(id):
    try:
        con = sql.connect('test.db')
        cur = con.cursor()
        print("............\nЗапрос к SQLite по проверке наличия в БД...\n")
        sqllite_select = f"""SELECT _id FROM users WHERE _id = {id}"""
        cur.execute(sqllite_select)

        if cur.fetchone() is None:
            print(f'Пользователь {id} не найден!')
            cur.close()
            return 0
        else:
            print(f'Пользователь {id} есть в БД.')
            cur.close()
            return 1
    except sql.Error as error:
        print("###Ошибка при работе с SQLite:", error)
    finally:
        if con:
            con.close()
            print("\nСоединение с SQLite закрыто.\n............")

def get_status(id):
    try:
        con = sql.connect('test.db')
        cur = con.cursor()
        print("............\nЗапрос к SQLite по получению статуса...\n")
        sqllite_select = f"""SELECT _status FROM users WHERE _id = {id}"""
        tmp = cur.execute(sqllite_select).fetchone()[0]
        if tmp is None:
            print(f'Пользователь {id} не найден!')
            cur.close()
            return -1
        else:
            print(f'Пользователь {id} есть в БД.')
            stat = tmp
            cur.close()
            return stat
    except sql.Error as error:
        print("###Ошибка при работе с SQLite:", error)
    finally:
        if con:
            con.close()
            print("\nСоединение с SQLite закрыто.\n............")

def get_code(stat, _class):
    try:
        con = sql.connect('test.db')
        cur = con.cursor()
        print("............\nЗапрос к SQLite по получению номера кода...\n")
        log = f"""SELECT code{stat} FROM 'type' WHERE _id = {_class}"""
        out = cur.execute(log).fetchone()[0]
        return out
    except sql.Error as error:
        print("###Ошибка при работе с SQLite:", error)
    finally:
        if con:
            con.close()
            print("\nСоединение с SQLite закрыто.\n............")

def hi(prof_id):
    try:
        con = sql.connect('test.db')
        cur = con.cursor()
        print("............\nЗапрос к SQLite по приветствию...\n")
        tp_select = f"""SELECT hi_text FROM 'type' WHERE _id = {prof_id}"""
        out = cur.execute(tp_select).fetchone()[0]
        return out
    except sql.Error as error:
        print("###Ошибка при работе с SQLite:", error)
    finally:
        if con:
            con.close()
            print("\nСоединение с SQLite закрыто.\n............")
def mess(_stat, type):
    try:
        con = sql.connect('test.db')
        cur = con.cursor()
        print("............\nЗапрос к SQLite по тексту...\n")
        tp_select = f"""SELECT text{_stat} FROM 'type' WHERE _id = {type}"""
        out = cur.execute(tp_select).fetchone()[0]
        print(out)
        return out
    except sql.Error as error:
        print("###Ошибка при работе с SQLite:", error)
    finally:
        if con:
            con.close()
            print("\nСоединение с SQLite закрыто.\n............")

def get_info(id):
    try:
        con = sql.connect('test.db')
        cur = con.cursor()
        print("............\nЗапрос к SQLite по информации...\n")
        sqllite_select = f"""SELECT _id FROM users WHERE _id = {id}"""
        cur.execute(sqllite_select)

        if cur.fetchone() is None:
            print(f'Пользователь {id} не найден!')
            return
        else:
            cur.execute(f"""SELECT * FROM users WHERE _id = {id}""")
            record = cur.fetchall()
            for row in record:
                print(f'ID: {row[0]}')
                print(f'Name: {row[1]}')
                print(f'Class: {row[2]}')
                print(f'Status: {row[3]}')

        cur.close()
    except sql.Error as error:
        print("###Ошибка при работе с SQLite:", error)
    finally:
        if con:
            con.close()
            print("\nСоединение с SQLite закрыто.\n............")


def change_status(id):
    try:
        con = sql.connect('test.db')
        cur = con.cursor()
        print("............\nЗапрос к SQLite по смене статуса...\n")
        sqllite_select = f"""SELECT _id FROM users WHERE _id = {id}"""

        cur.execute(sqllite_select)
        if cur.fetchone() is None:
            print(f'Пользователь {id} не найден!')
            return
        else:
            l_stat = cur.execute(f"""SELECT _status FROM users WHERE _id = {id}""").fetchone()[0]
            if l_stat is None:
                sqllite_update = f"""UPDATE users
                                                            SET _status = 1
                                                            WHERE _id = {id}"""
                cur.execute(sqllite_update)
                con.commit()
                print(f'Статус {id} обновлён с {l_stat} на {1}.')
            elif l_stat < 9:
                new_stat = l_stat+1
                sqllite_update = f"""UPDATE users
                                            SET _status = {new_stat}
                                            WHERE _id = {id}"""
                cur.execute(sqllite_update)
                con.commit()
                print(f'Статус {id} обновлён с {l_stat} на {new_stat}.')
            else:
                print(f'Статус {id} уже на максимуме.')
        cur.close()
    except sql.Error as error:
        print("###Ошибка при работе с SQLite:", error)
    finally:
        if con:
            con.close()
            print("\nСоединение с SQLite закрыто.\n............")


def chim_or_bio(id):
    try:
        con = sql.connect('test.db')
        cur = con.cursor()
        print("............\nЗапрос к SQLite по получению номера науки...\n")
        sqllite_prof = f"""SELECT _class FROM 'users' WHERE _id = {id}"""
        prof_name = cur.execute(sqllite_prof).fetchone()[0]

        if prof_name is None:
            print(f'Пользователь {id} не найден!')
            return
        else:
            if prof_name == 'биология':
                return 1
            elif prof_name == 'химия':
                return 2
            else:
                return 3
        cur.close()
    except sql.Error as error:
        print("###Ошибка при работе с SQLite:", error)

    finally:
        if con:
            con.close()
            print("\nСоединение с SQLite закрыто.\n............")