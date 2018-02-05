from mysql.connector import MySQLConnection

def send():
	conn = MySQLConnection( host = '10.0.10.220',
	                            database = 'ICP',
	                            user = 'tran',
	                            password = 'GreenX0123')
	curs = conn.cursor()

	name = 'test send data'
	custID = 1

	add_proj = ("CALL addProj(%s, %s)")

	data = (name, custID)

	curs.execute(add_proj, data)

	conn.commit()

	curs.close()
	conn.close()