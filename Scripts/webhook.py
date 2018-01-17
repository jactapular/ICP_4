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

# temp 
tmpH = request.data["DevEUI_uplink"]["payload_hex"]
tmpH = tmpH[0:2]
tmp = int(tmpH, 16)


#humidity
humH = request.data["DevEUI_uplink"]["payload_hex"]
humH = humh[2:2]
hum = int(humH, 16)



add_read = ("CALL addRead(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

data = (uID, time, 1, 1, float(tmp), float(hum), 0.0, 0.0, 0.0, 0.0)

curs.execute(add_read, data)

conn.commit()

curs.close()
conn.close()
