from mysql.connector import MySQLConnection, Error



###### NOT REQUIRED ######
#from configparser import ConfigParser
#from python_mysql_dbconfig import read_db_config
# from datetime import date, datetime, timedelta, time

###### FOR TESTING ######
from time import strftime, sleep
    try:
    db_config = {
        'host' = '10.0.10.220:3306'
        'database' = 'ICP'
        'user' = 'trans'
        'password' = 'GreenX0123'
    }
            # # unit ID
            # uID = request.view_args["Time"]
            # # time
            # time = request.view_args["DevAddr"]
            # # temp 
            # tmp = 
            # #humidity
            # hum =
    # unit ID
    uID = 0x00540006;
    # time
    time = strftime('%Y-%m-%d %H:%M:%S')
    # temp = 26
    tmp = 0x1A
    #humidity = 37
    hum = 25
        conn = MySQLConnection(**db_config)
        cursor = conn.cursor()
        cursor.execute("CALL addRead(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(uID, time, 1, 1, int(tmp, 16), int(hum, 16), 0.0, 0.0, 0.0, 0.0))
        print "add reading at: ", t
        conn.commit()
    except Error as error:
        print(error)

    finally:
        cursor.close()
        conn.close()