import psycopg2

#reference of structure in sqlLite https://github.com/Priler/accountant/blob/main/db.py
#reference of psycopg2 https://github.com/pythontoday/python_postgresql_connection/blob/master/main.py

class BotDB:

    def __init__(self, host, user, password, db_name):
        try:
        # connect to exist database
            self.connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name    
            )
            self.connection.autocommit = True
        except Exception as _ex:
            print("[INFO] Error while working with PostgreSQL", _ex)

    def user_exists(self, user_id): #проверяем, есть ли пользователь в базе
        result = self.cursor.execute("SELECT id FROM users WHERE user_id = %user_id")
        return bool(len(result.fetchall()))
    


    def close(self): #Закрываем соединение с БД
        self.connection.close()