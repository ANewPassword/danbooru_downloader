# -*- coding: utf-8 -*-

import sqlite3
from time import time
from func.fileio import file_mkdir

class MySQL: # 明明是sqllite却用mysql当类名，何尝不是一种ntr
    def __init__(self, program_path, template_name):
        self.program_path = program_path
        self.template_name = template_name
        self.default_table_name = 'download_record'
        file_mkdir(self.program_path + '/db/')

    def connect(self):
        # 连接到数据库（如果数据库不存在，则会创建一个新的数据库文件）
        self.conn = sqlite3.connect('%s/db/%s.db' % (self.program_path, self.template_name))
        # 创建一个游标对象，用于执行 SQL 语句
        self.cursor = self.conn.cursor()
        self.conn.row_factory = sqlite3.Row
        return True

    def install(self, table = None):
        if table == None:
            table = self.default_table_name
        # 创建表
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} (id TEXT PRIMARY KEY NOT NULL, md5 TEXT DEFAULT '', timestamp TEXT DEFAULT '', description TEXT DEFAULT '')")
        # 提交事务（将数据保存到数据库）
        self.conn.commit()
        return True

    def insert(self, table = None, **data):
        if table == None:
            table = self.default_table_name
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        values = tuple(data.values())
        query = f'INSERT INTO {table} ({columns}) VALUES ({placeholders})'
        if data:
            self.cursor.execute(query, values)
        else:
            self.cursor.execute(f"INSERT INTO {table} DEFAULT VALUES")
        self.conn.commit()
        if self.cursor.rowcount == 0:
            return False
        return True

    def delete(self, table = None, **conditions):
        if table == None:
            table = self.default_table_name
        where_clause = ' AND '.join([f'{column} = ?' for column in conditions.keys()])
        values = tuple(conditions.values())
        query = f'DELETE FROM {table} WHERE {where_clause}'
        self.cursor.execute(query, values)
        self.conn.commit()
        if self.cursor.rowcount == 0:
            return False
        return True

    def select(self, table = None, columns = '*', **conditions):
        if table == None:
            table = self.default_table_name
        column_list = ', '.join(columns) if isinstance(columns, list) else columns
        where_clause = ' AND '.join([f'{column} = ?' for column in conditions.keys()])
        values = tuple(conditions.values())
        query = f'SELECT {column_list} FROM {table}'
        if conditions:
            query += f' WHERE {where_clause}'
        self.cursor.execute(query, values)
        result = self.fetch_all_as_dict()
        return result

    def update(self, table = None, condition = None, **data):
        if table == None:
            table = self.default_table_name
        if condition == None:
            return False
        condition_str = ""
        condition_values = []
        set_clause = ', '.join([f'{column} = ?' for column in data.keys()])
        values = list(data.values())
        for key, value in condition.items():
            condition_str += f"{key} = ? AND "
            condition_values.append(value)
        condition_str = condition_str.rstrip("AND ")
        values.extend(condition_values)
        values = tuple(values)
        query = f'UPDATE {table} SET {set_clause} WHERE {condition_str}'
        self.cursor.execute(query, values)
        self.conn.commit()
        if self.cursor.rowcount == 0:
            return False
        return True

    def fetch_all_as_dict(self):
        columns = [desc[0] for desc in self.cursor.description]  # 获取列名
        rows = self.cursor.fetchall()
        results = []
        for row in rows:
            result = {}
            for i, column in enumerate(columns):
                result[column] = row[i]
            results.append(result)
        return results

    def count(self, table = None):
        if table == None:
            table = self.default_table_name
        sql = f"SELECT COUNT(*) FROM {table}"
        self.cursor.execute(sql)
        count = self.cursor.fetchone()[0]
        return count

    def insert_post(self, id, md5, timestamp = None, description = None, table = None):
        if table == None:
            table = self.default_table_name
        if timestamp == None:
            timestamp = int(time())
        if description == None:
            description = ''
        return self.insert(table, id = id, md5 = md5, timestamp = timestamp, description = description)

    def delete_post_by_id(self, id, table = None):
        if table == None:
            table = self.default_table_name
        return self.delete(table, id = id)

    def select_post_by_id(self, id, table = None):
        if table == None:
            table = self.default_table_name
        return self.select(table, id = id)

    def update_post_by_id(self, id, update_data, table = None):
        if table == None:
            table = self.default_table_name
        return self.update(table, {'id': id}, **update_data)

    def close(self):
        # 关闭游标和数据库连接
        self.cursor.close()
        self.conn.close()