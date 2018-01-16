from mysql.connector import MySQLConnection, Error
###### FOR TESTING ######
from time import strftime, sleep

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
uID = '0x00540006';
    # time
time = strftime('%Y-%m-%d %H:%M:%S')
tmp = 37.01
#tmp = 0x1A
hum = 52.01
#hum = 0x25

add_read = ("CALL addRead(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

data = (uID, time, 1, 1, tmp, hum, 0.0, 0.0, 0.0, 0.0)

curs.execute(add_read, data)

conn.commit()

curs.close()
conn.close()
