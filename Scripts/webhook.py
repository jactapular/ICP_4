from mysql.connector import MySQLConnection, Error
###### NOT REQUIRED ######
#from configparser import ConfigParser
#from python_mysql_dbconfig import read_db_config
# from datetime import date, datetime, timedelta, time

###### FOR TESTING ######
from time import strftime, sleep

#try:


conn = MySQLConnection( host = '10.0.10.220',
                            database = 'ICP',
                            user = 'tran',
                            password = 'GreenX0123')
curs = conn.cursor()

    # # unit ID
    # # uID = request.data["Time"]
    # # time
    # time = request.view_args["DevAddr"]
    # # temp 
    # tmp = request.data["DevEUI_uplink"."payload_hex"."mydata[0]"]
    # tmp = int(tmp, 16)
    # #humidity
    # hum = request.data["DevEUI_uplink"."payload_hex"."mydata[1]"]
    # hum = int(hum, 16)
    # unit ID
uID = str(0x00540006);
    # time
time = strftime('%Y-%m-%d %H:%M:%S')
    # temp = 26
tmp = 0x1A
    #humidity = 37
hum = 0x25

add_read = ("CALL addCust('testy Mcgee', 'test@email.com')")
#data = ('0123', time, 1, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

#add_read = ("CALL addRead(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
#data = ('0123', time, 1, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)


curs.execute(add_read)

conn.commit()
#except Error as error:
#print(error)

#finally:
curs.close()
conn.close()
