import psycopg2

class BotDB:

    def __init__(self, host, user, password, db_name):
        try:
        # connect to exist database
            connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name    
            )
            connection.autocommit = True
        except Exception as _ex:
            print("[INFO] Error while working with PostgreSQL", _ex)

    def user_exists(self, user_id): #проверяем, есть ли пользователь в базе
        result = self.cursor.execute("SELECT id FROM users WHERE user_id = %user_id")
        return bool(len(result.fetchall()))
    


    def close(self): #Закрываем соединение с БД
        self.connection.close()