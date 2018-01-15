from mysql.connector import MySQLConnection, Error



###### NOT REQUIRED ######
#from configparser import ConfigParser
#from python_mysql_dbconfig import read_db_config
# from datetime import date, datetime, timedelta, time
# from time import strftime, sleep
    try:
    db_config = {
        'host' = '10.0.10.220:3306'
        'database' = 'ICP'
        'user' = 'trans'
        'password' = 'GreenX0123'
    }
    
    t = request.view_args["Time"]
    
        conn = MySQLConnection(**db_config)
        if request.method == 'GET':
            cursor = conn.cursor()
            cursor.execute("CALL addRead(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(1, t, 1, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0))
            print "add reading at: ", t
            conn.commit()
    except Error as error:
        print(error)

    finally:
        cursor.close()
        conn.close()