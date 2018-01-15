def WoodsideSensor(moteID,action):
    # Create log of data
    params = {
    'dbname':'woodsideweek',
    'user':'woodsideclient',
    'password':'wssensor',
    'host':'10.0.10.99',
    'port':5432
    }
    f = open(os.path.join(config.UPLOAD_FOLDER, 'WoodsideSensor.log'), "a")
    f.write(request.data + "\n")
    f.close()
    
    
    connection = psycopg2.connect(**params)
    cur = connection.cursor()
    resp = ""
    
    if request.method == 'GET':
        if (request.view_args["action"] == "status"):
   cur.execute("SELECT status, comment FROM sensors WHERE name=\'"+moteID+"\'")
            resp = cur.fetchone()
     
    if request.method == 'POST':
        if (request.view_args["action"] == "flip"):
            cur.execute("UPDATE sensors SET status=3 WHERE name=\'"+moteID+"\'"+" AND status = 1")
            cur.execute("UPDATE sensors SET status=1 WHERE name=\'"+moteID+"\'"+" AND status = 0")
            cur.execute("UPDATE sensors SET status=0 WHERE name=\'"+moteID+"\'"+" AND status = 3")
            cur.execute("SELECT status, comment FROM sensors WHERE name=\'"+moteID+"\'")
            resp = cur.fetchone()
        if (request.view_args["action"] == "on"):
            cur.execute("SELECT * FROM statuschange")
            previousComments = cur.fetchall()
            cur.execute("UPDATE sensors SET status=1, comment=\'"+request.data+"\' WHERE name=\'"+moteID+"\'")
            cur.execute("SELECT status, comment  FROM sensors WHERE name=\'"+moteID+"\'")
            resp = cur.fetchone()
            cur.execute("INSERT INTO statuschange(newstatus,comment) VALUES ('on','"+request.data+"\')")
        if (request.view_args["action"] == "off"):
            cur.execute("UPDATE sensors SET status=0, comment=\'"+request.data+"\' WHERE name=\'"+moteID+"\'")
            cur.execute("SELECT status, comment  FROM sensors WHERE name=\'"+moteID+"\'")
            resp = cur.fetchone()
            cur.execute("INSERT INTO statuschange(newstatus,comment) VALUES ('off','"+request.data+"\')")

    connection.commit()
    cur.close()
    connection.close()
    if resp[0] == 0:
        strresponse = "Sensor disabled."
    if resp[0] == 1:
        strresponse = "Sensor enabled."
    if request.method == 'GET':
        strresponse = strresponse + "\n" + str(resp[1]) 
    #rsp = Response(
    return str(strresponse)
