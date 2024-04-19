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
            self.connection.autocommit = True
        except Exception as _ex:
            print("[INFO] Error while working with PostgreSQL", _ex)
        finally:
            self.cursor = self.connection.cursor()
            self.connection.autocommit = True
        

    def user_exists(self, user_id): #проверяем, есть ли пользователь в базе
        try:
            self.cursor.execute(f"SELECT user_id FROM users WHERE user_id = {user_id};")
        except Exception as _ex: 
            return False
        finally:
            return True
    
    def add_user(self, user_id, lifestyle, age, height, weight, gender): #создангие пользователя
        if not(self.user_exists(user_id)):
            self.cursor.execute(f"""INSERT INTO your_table_name (user_id, lifestyle, age, height, weight, gender)
                                VALUES ({user_id}, {lifestyle}, {age}, {height}, {weight}, {gender});""")
    
    def delete_user(self, user_id):
        self.cursor.execute(f"""DELETE FROM users
                            WHERE user_id = {user_id};""")

    def get_data(self, user_id, within="all"):
        result = ""
        try:
            result = self.cursor.execute(f"""SELECT {within} 
                                         FROM users 
                                         WHERE user_id = {user_id}""")
        except psycopg2.Error as e:
            pass
        return result


    def __del__(self): #Закрываем соединение с БД
        self.connection.close()

class foodDB:
    pass