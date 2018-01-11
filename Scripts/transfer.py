# script to listen for new packets from sensors and forward to mysql database

from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config
from datetime import date, datetime, timedelta, time
from time import strftime
 
try:
    db_config = read_db_config()
    conn = MySQLConnection(**db_config)

    # t = datetime.now().date()
    t = strftime('%Y-%m-%d %H:%M:%S')

    cursor = conn.cursor()
    cursor.execute("CALL addRead(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(1, t, 1, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0))

    conn.commit()
except Error as error:
    print(error)

finally:
    cursor.close()
    conn.close()
