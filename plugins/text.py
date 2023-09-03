import sqlite3 as sql

def ini():
    try:
        con = sql.connect('test.db')
        cur = con.cursor()
        print("............\nЗапрос к SQLite по импорту...\n")
        cur.execute("CREATE TABLE IF NOT EXISTS 'type' ('_id' INTEGER,"
                    "                                   '_name_type' STRING, "
                    "                                   'hi_text' TEXT,"
                    "                                   'code1' TEXT,"
                    "                                   'text1' TEXT,"
                    "                                   'code2' TEXT,        "
                    "                                   'text2' TEXT,        "
                    "                                   'code3' TEXT,        "
                    "                                   'text3' TEXT,        "
                    "                                   'code4' TEXT,        "
                    "                                   'text4' TEXT,        "
                    "                                   'code5' TEXT,        "
                    "                                   'text5' TEXT,        "
                    "                                   'code6' TEXT,        "
                    "                                   'text6' TEXT,        "
                    "                                   'code7' TEXT,        "
                    "                                   'text7' TEXT,        "
                    "                                   'code8' TEXT,        "
                    "                                   'text8' TEXT,        "
                    "                                   'code9' TEXT,        "
                    "                                   'text9' TEXT        "
                    ")")



    except sql.Error as error:
        print("###Ошибка при работе с SQLite:", error)
    finally:
        if con:
            con.close()
            print("\nСоединение с SQLite закрыто.\n............")