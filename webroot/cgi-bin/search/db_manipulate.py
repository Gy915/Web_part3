import sqlite3
import os

DB_PATH = os.path.expanduser('~/.cgi/student.db')
class Student:

    # UID = None, NAME = None, AGE = None, SEX = None, CLASS = None, TEACHER = None, SCORE = None, VALID = None, RESERVED = None
    def __init__(self, UID, NAME, AGE, SEX, CLASS, TEACHER, SCORE, VALID, RESERVED):
        self._table = {}
        self._table['UID']      = UID
        self._table['NAME']     = NAME
        self._table['AGE']      = AGE
        self._table['SEX']      = SEX
        self._table['CLASS']    = CLASS
        self._table['TEACHER']  = TEACHER
        self._table['SCORE']    = SCORE
        self._valid             = VALID
        self._reserved          = RESERVED
    
    def get_all(self) -> tuple:
        return self._table['UID'], self._table['NAME'], self._table['AGE'], self._table['SEX'], self._table['CLASS'], self._table['TEACHER'], self._table['SCORE']

    def get_val(self) -> tuple:
        return self._valid, self._table[self._valid]

    def get_res(self) -> tuple:
        return self._reserved, self._table[self._reserved]

class DB:
    def __init__(self):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        self._create_table()
    
    def _create_table(self):
        try:
            conn = sqlite3.connect(DB_PATH)
            conn.execute('''
                CREATE TABLE IF NOT EXISTS STUDENT(
                    UID     INTEGER PRIMARY KEY,
                    NAME    TEXT    NOT NULL,
                    AGE     INTEGER,
                    SEX     TEXT,
                    CLASS   TEXT,
                    TEACHER TEXT,
                    SCORE   TNREGER
                );
            ''')
            conn.commit()
        except:
            raise Exception('创建表发生错误')
    
    def db_select(self, stu) -> list:
        try:
            key, value = stu.get_val()
            conn = sqlite3.connect(DB_PATH)
            cur = conn.execute(f'SELECT * FROM STUDENT WHERE {key} = {value}')
            conn.commit()
            return cur
        except:
            raise Exception('查找数据发生错误')
    
    def db_insert(self, stu) -> None:
        try:
            res = stu.get_all()
            conn = sqlite3.connect(DB_PATH)
            conn.execute('INSERT INTO STUDENT VALUES (?, ?, ?, ?, ?, ?, ?)', res)
            conn.commit()
            conn.close()
        except:
            raise Exception('插入数据发生错误')
    
    def db_update(self, stu) -> None:
        try:
            key1, value1 = stu.get_val()
            key2, value2 = stu.get_res()
            conn = sqlite3.connect(DB_PATH)
            conn.execute('UPDATE STUDENT SET ? = ?  WHERE ? = ?', (key1, value1, key2, value2))
            conn.commit()
        except:
            raise Exception('更新数据发生错误')
    
    def db_delete(self, stu) -> None:
        try:
            key, value = stu.get_val()
            conn = sqlite3.connect(DB_PATH)
            conn.execute('DELETE * FROM STUDENT WHERE ? = ?', (key, value))
            conn.commit()
        except:
            raise Exception('删除数据发生错误')