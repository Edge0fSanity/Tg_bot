import psycopg2
import logging


#reference of structure in sqlLite https://github.com/Priler/accountant/blob/main/db.py
#reference of psycopg2 https://github.com/pythontoday/python_postgresql_connection/blob/master/main.py

class fitnessDB:

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
             logging.info("[INFO] Error while working with PostgreSQL", _ex)
        

    def user_exists(self, user_id) -> bool: #проверяем, есть ли пользователь в базе
        with self.connection.cursor() as cursor:
            try:
            
                cursor.execute("SELECT user_id FROM users WHERE user_id = %s;", (user_id, ))
            except Exception as _ex: 
                self.connection.rollback()
                return False
            finally:
                return bool(cursor.fetchone())
    
    def delete_user(self, user_id):
        with self.connection.cursor() as cursor:
            cursor.execute("""DELETE FROM users
                            WHERE user_id = %s;""", (user_id, ))
            self.connection.commit()


    def add_user(self, user_id, user_name, lifestyle, age, height, weight, gender, kkal) -> bool: #создангие пользователя
        """"
        delete old and creates new user with 
        user_id as primary key
        """
        try:
            self.delete_user(user_id)
            with self.connection.cursor() as cursor:
                cursor.execute("""INSERT INTO users (user_id, user_name, lifestyle, age, height, weight, gender, kkal)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);""", (user_id, user_name, lifestyle, age, height, weight, gender, kkal))
                self.connection.commit()
                return True
        except Exception as _ex: 
            self.connection.rollback()
            logging.info("[INFO] Error while working with PostgreSQL add_user function", _ex)
            return False





    def get_data(self, user_id) -> tuple:
        result = (0,0,0,0,0,0,0,0)
        try:
            with self.connection.cursor() as curs:
                curs.execute("""SELECT * 
                                FROM users 
                                WHERE user_id = %s""", (user_id, ))
                result = curs.fetchone()
        except psycopg2.Error as e:
            pass
        return result
    
    def getfood(self, kkall: float) -> str:
        """"returns 'Not found' when sql output is not provided"""

        result = "Not found"

        try:
            with self.connection.cursor() as curs:
                curs.execute("""SELECT name FROM food
                                WHERE kkal = %s
                                ORDER BY RANDOM()
                                LIMIT 1;""", (kkall, ))
                result = curs.fetchone()
        except psycopg2.Error as e:
            pass
        return result
        

    def __del__(self): #Закрываем соединение с БД
        self.connection.close()
