from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config
 
def insert_reading():
    query = "CALL addRead(1, '2018-01-9 18:55:00', 1, 1, 0.00, 0.00, 0.0, 0.0, 0.0, 0.0)"

 
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)

        cursor = conn.cursor()
        cursor.execute(query)

        if cursor.lastrowid:
           print('last insert id', cursor.lastrowid)
        else:
           print('last insert id not found')

        conn.commit()
    except Error as error:
        print(error)

    finally:
        cursor.close()
        conn.close()

def main():
   insert_reading()