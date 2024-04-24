import psycopg2


#reference of structure in sqlLite https://github.com/Priler/accountant/blob/main/db.py
#reference of psycopg2 https://github.com/pythontoday/python_postgresql_connection/blob/master/main.py

class usersDB:

    def __init__(self):
        try:
        # connect to exist database
            self.connection = psycopg2.connect(
            host="192.168.1.11",
            user="fitness",
            password="reanimator2401",
            database="fitness"    
            )
        except Exception as _ex:
            print("[INFO] Error while working with PostgreSQL", _ex)
        

    def user_exists(self, user_id): #проверяем, есть ли пользователь в базе
        with self.connection.cursor() as cursor:
            try:
            
                cursor.execute("SELECT user_id FROM users WHERE user_id = %s;", (user_id, ))
            except Exception as _ex: 
                self.connection.rollback()
                return False
            finally:
                return bool(cursor.fetchone())
    
    def add_user(self, user_id, lifestyle, age, height, weight, gender): #создангие пользователя
        if True:
            with self.connection.cursor() as cursor:
                cursor.execute("""INSERT INTO users (user_id, lifestyle, age, height, weight, gender)
                                VALUES (%s, %s, %s, %s, %s, %s);""", (user_id, lifestyle, age, height, weight, gender))
                self.connection.commit()


    def delete_user(self, user_id):
        with self.connection.cursor() as cursor:
            cursor.execute(f"""DELETE FROM users
                            WHERE user_id = {user_id};""")
            self.connection.commit()


    def get_data(self, user_id, within="all"):
        result = ""
        try:
            with self.connection.cursor() as cursor:
                result = cursor.execute("""SELECT %s 
                                         FROM users 
                                         WHERE user_id = %s""", (within, user_id))
        except psycopg2.Error as e:
            pass
        return result


    def __del__(self): #Закрываем соединение с БД
        self.connection.close()

class foodDB:
    pass