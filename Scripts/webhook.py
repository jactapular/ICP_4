from mysql.connector import MySQLConnection
from time import strftime, sleep

conn = MySQLConnection( host = '10.0.10.220',
                            database = 'ICP',
                            user = 'tran',
                            password = 'GreenX0123')
curs = conn.cursor()

# unit ID
uID = request.data["DevEUI_uplink"]["DevAddr"]

# time
time = strftime('%Y-%m-%d %H:%M:%S')
#may be in the wrong format ie  2017-07-20T07:13:24.40+02:00
#time = request.data["DevEUI_uplink"]["Time"]

pl = request.data["DevEUI_uplink"]["payload_hex"]

#ProjectID
pID = (int(pl[0:2], 16))

#LocationID
lID = (int(pl[2:4], 16))

#temp 
tmp = (float(int(pl[4:8], 16)))/100

#humidity
lux = (float(int(pl[8:12], 16)))

#ints
three = (float(int(pl[12:16], 16)))

four = (float(int(pl[16:20], 16)))

#foats
five = (float(int(pl[20:24], 16)))/100

six = (float(int(pl[24:28], 16)))/100


add_read = ("CALL addRead(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

data = (uID, time, pID, lID, tmp, lux, three, four, five, six)

curs.execute(add_read, data)

conn.commit()

curs.close()
conn.close()
