

from flask import Flask, request, template_rendered, Response
from flask_cors import CORS
from ciscospark.bot import SparkBot
from ciscospark import messages
from datetime import datetime
from mysql.connector import MySQLConnection
from time import strftime
# Interact with the OS
import os
import subprocess
import requests
import json


# Local configuration settings
import config

# For Woodside Week
import psycopg2

def setup_webhook(bearer_token, webook_name, webhook_secret, webhook_target_url):
    b = SparkBot(bearer_token)
    b.secret = webhook_secret
    b.delete_webhook(webook_name)
    b.create_webhook(webook_name, webhook_target_url)


app = Flask(__name__)
cors = CORS(app, resources={r"/elastic": {"origins": "*"}})

@app.route('/')
def base():
    return template_rendered('base.html')


@app.route('/ansibot', methods=['POST'])
def ansibot():
    # Setup ansiBot
    token = config.ansibot_bearer_token
    b = SparkBot(token)

    # Create log of data
    f = open(os.path.join(config.UPLOAD_FOLDER, 'ansibot.log'), "a")
    f.write(request.data + "\n")
    f.close()

    # webhook memberships.created
    req_resource = request.json['resource']
    req_event = request.json['event']
    req_roomId = request.json['data']['roomId']
    if req_resource == 'memberships' and req_event == 'created':
        text = 'Hello, I am *' + b.bot_name + '*. I have come to Earth to party and to help with IT Automation. Feel free to ask me what I can help you with! \n- Say **help**, if you are talking 1-on-1 with me. \n- Say **@CIIC Ansible Bot help**, if you are in a room.'
        tmp_dict = messages.create(token, roomId=req_roomId, markdown=text)
        return Response()

    # verify message is not from the bot itself (loop prevention)
    msg_sender = request.json['data']['personEmail']
    if msg_sender == b.bot_email:
        return Response()

    # parse incoming message
    msg = b.get_webhook_message()
    msg_text = msg['text'].replace('EventAssist', '')
    msg_sender = msg['personEmail']
    msg_senderId = msg['personId']
    msg_roomType = msg['roomType']
    msg_roomId = msg['roomId']

    # 'help' command
    if msg_text == 'help':

        text = 'Sure thing *' + msg_sender + '*. Here is a list of things I can help you with! \n- **hosts** - Get a list of host groups. \n- **playbooks** - Get a list of playbooks. \n- **run** *playbook* *hostgroup* - Run a playbook on a host group.'
        tmp_dict = messages.create(token, roomId=msg_roomId, markdown=text)

    # 'hosts' lists all host groups
    if msg_text == 'hosts':

        list_text = ''
        p = subprocess.Popen('ansible localhost -m debug -a \'var=groups.keys()\'', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in p.stdout.readlines():
            list_text += line + "\n"
        retval = p.wait()

        text = 'Here is a list of host groups:\n'
        tmp_dict = messages.create(token, roomId=msg_roomId, markdown=text)
        tmp_dict = messages.create(token, roomId=msg_roomId, markdown=list_text)

    # 'playbooks' lists all playbooks
    if msg_text == 'playbooks':

        list_text = ''
        p = subprocess.Popen('ls /etc/ansible/playbooks/', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in p.stdout.readlines():
            list_text += line + "\n"
        retval = p.wait()

        text = 'Here is a list of playbooks:\n'
        tmp_dict = messages.create(token, roomId=msg_roomId, markdown=text)
        tmp_dict = messages.create(token, roomId=msg_roomId, markdown=list_text)

    # 'apt-update' updates all servers
    if msg_text == 'apt-update':

        text = 'Running Playbook....:\n'
        tmp_dict = messages.create(token, roomId=msg_roomId, markdown=text)

        list_text = ''
        command = 'sudo ansible-playbook /etc/ansible/playbooks/ubuntu_upgrade.yml -f 10 --extra-vars \"ansible_sudo_pass=C1sc0123\"'
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in p.stdout.readlines():
            list_text += line + "\n"
        retval = p.wait()

        text = 'Result of update:\n'
        tmp_dict = messages.create(token, roomId=msg_roomId, markdown=text)
        tmp_dict = messages.create(token, roomId=msg_roomId, markdown=list_text)

    return Response()


@app.route('/actility', methods=['POST'])
def actility():

    # Create log of data
    f = open(os.path.join(config.UPLOAD_FOLDER, 'actility.log'), "a")
    f.write(request.data + "\n")
    f.close()

    # POST the actility data through to EFF
    requests.post('http://134.7.246.99:8020/actility?value', data=json.dumps(request.data))

    return Response()

@app.route('/FDP', methods=['POST'])
def FDP():

    # Create log of data
    f = open(os.path.join(config.UPLOAD_FOLDER, 'FDP.log'), "a")
    f.write(request.data + "\n")
    f.close()

    # POST the actility data through to EFF
    requests.post('http://134.7.246.99:8020/FDP?value', data=json.dumps(request.data))
    requests.post('http://172.20.15.50:8020/FDP?value', data=json.dumps(request.data))
    return Response()

@app.route('/FDPWoW', methods=['POST'])
def FDPWoW():

    #create log of data
    f = open(os.path.join(config.UPLOAD_FOLDER, 'FDPWoW.log'), "a")
    f.write(request.data + "\n")
    f.close()

    # POST the actility data through to EFF
    requests.post('http://134.7.246.99:8020/FDPWOW?value', data=json.dumps(request.data))
    requests.post('http://172.20.15.50:8020/FDPWOW?value', data=json.dumps(request.data))
    return Response()

@app.route('/woodside', methods=['POST'])
def woodside():
# used for the parsing of incomming JSON data from woodside for woodside week 

    # Create log of data
    f = open(os.path.join(config.UPLOAD_FOLDER, 'woodside.log'), "a")
    f.write(request.data + "\n")

    utc_time = datetime.strptime(request.json["GatewayTS"], "%Y-%m-%dT%H:%M:%S.%fZ")
    epoch_time = (utc_time - datetime(1970, 1, 1)).total_seconds()
    epoch_time = int(epoch_time)
    epoch_time = str(epoch_time) + "000"

    data=json.dumps(request.data)

    newData = {}
    if (request.json["SensorLetter"] == "a" or request.json["SensorLetter"] =="b"):
    	newData['GatewayTS'] = epoch_time
    	newData['MoteID'] = request.json["MoteID"]
    	newData['SigStrength'] = request.json["SigStrength"]
    	newData['DataRate'] = request.json["DataRate"]

    	if (request.json['Visualise'] == 'Y'):
    	    newData['Visualiseint'] = 1
        if (request.json['Visualise'] == 'N'):
    	    newData['Visualiseint'] = 0

    	newData['SensorLetter'] = request.json["SensorLetter"]
    	newData['Temperature'] = request.json["Temperature"]
    	newData['msgCnt'] = request.json["msgCnt"]
    	json_newData = json.dumps(newData)

    if (request.json["SensorLetter"] == "A"):
        newData['MoteID'] = request.json["MoteID"]
        newData['SigStrength'] = request.json["SigStrength"]
        newData['DataRate'] = request.json["DataRate"]

        if (request.json['Visualise'] == 'Y'):
            newData['Visualiseint'] = 1 
        if (request.json['Visualise'] == 'N'):
            newData['Visualiseint'] = 0

    	newData['GatewayTS'] = epoch_time
     	newData['SensorLetter'] = "f"
    	newData['Frequency'] = request.json["Frequency"]
    	newData['Amplitude'] = request.json["Amplitude"]
        newData['msgCnt'] = request.json["msgCnt"]
   	json_newData = json.dumps(newData)


    requests.post('http://10.0.10.173:9200/woodside/1', json_newData)

    token = config.ansibot_bearer_token
    messages.create(token, toPersonEmail='Tom.Deruijter@curtin.edu.au', markdown=data)
    messages.create(token, toPersonEmail='Tom.Deruijter@curtin.edu.au', markdown=json_newData)
    f.write("new response is:" + json_newData + "\n")
    f.close()
    return Response()

@app.route('/kibana', methods=['POST'])
def kibana():
# Used to forward JSON objects to Kibana to create visualisations

    # Create log of data
    f = open(os.path.join(config.UPLOAD_FOLDER, 'kibana.log'), "a")
    f.write(request.data + "\n")
    f.close()

    requests.post('http://10.0.10.173:4000/api/new', json=json.loads(request.data),headers={'Content-type':'application/json'})

    return Response()

@app.route('/elastic', methods=['POST'])
def elastic():
#Used to query elasticsearch for the woodside week app, allowing for the return of a JSON object from the local server
# to the wider internet

    # Create log of data
    f = open(os.path.join(config.UPLOAD_FOLDER, 'elastic.log'), "a")
    f.write(request.data + "\n")
    f.close()

    # POST the actility data through to EFF
    resp = requests.post('http://10.0.10.173:9200/woodside/_search', json=json.loads(request.data),headers={'Content-type':'application/json'})

    return resp.text

@app.route('/mdot_demo', methods=['POST'])
def mdot_demo():

    # Create log of data
    f = open(os.path.join(config.UPLOAD_FOLDER, 'mdot_demo.log'), "a")
    f.write(request.data + "\n")
    f.close()

    # POST the actility data through to EFF
    requests.post('http://134.7.246.99:8020/mdot_demo?value', data=json.dumps(request.data))

    return Response()

@app.route('/r2cc_post', methods=['POST'])
def r2cc_post():

    # Create log of data
    f = open(os.path.join(config.UPLOAD_FOLDER, 'r2cc_post.log'), "a")
    f.write(request.data + "\n")
    f.close()

    # POST the actility data through to EFF
    requests.post('http://134.7.246.110/post', json=json.loads(request.data),headers={'Content-type':'application/json'})


    return Response()


@app.route('/air/sparkbot', methods=['POST'])
def air_sparkbot():

    # Create log of data
    f = open(os.path.join(config.UPLOAD_FOLDER, 'air_sparkbot.log'), "a")
    f.write(request.data + "\n")
    f.close()

    #note the json=json and content-type header
    requests.post('http://10.0.10.162:8080', json=json.loads(request.data),headers={'Content-type':'application/json'})
    return Response()


@app.route('/air/interactor', methods=['POST'])
def air_test():

    # Create log of data
    f = open(os.path.join(config.UPLOAD_FOLDER, 'air_interactor.log'), "a")
    f.write(request.data + "\n")
    f.close()

    if (request.json["action"] == "setup"):
	requests.get('http://10.0.10.162:8081/api/setup')

    if (request.json["action"] == "delete"):
	requests.get('http://10.0.10.162:8081/api/delete')

    return Response()



@app.route('/CurtinChatBot', methods=['POST'])
def CurtinChatBot():

    # Create log of data
    f = open(os.path.join(config.UPLOAD_FOLDER, 'CurtinChatBot.log'), "a")
    f.write(request.data + "\n")
    f.close()

    #note the json=json and content-type header
    requests.post('http://10.0.10.11:8123', json=json.loads(request.data),headers={'Content-type':'application/json'})
    return Response()

@app.route('/HashtagSparkbot', methods=['POST'])
def HashtagSparkbot():

    # Create log of data
    f = open(os.path.join(config.UPLOAD_FOLDER, 'HashtagSparkbot.log'), "a")
    f.write(request.data + "\n")
    f.close()

    requests.post('http://10.0.10.160:1667', json=json.loads(request.data),headers={'Content-type':'application/json'})
    return Response()

@app.route('/WoodsideSensor/<moteID>/<action>', methods=['GET', 'POST'])
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
    
    sensorObject = json.dumps(request.data)
    
    connection = psycopg2.connect(**params)
    cur = connection.cursor()
    resp = ""
    
    if request.method == 'GET':
        if (request.view_args["action"] == "status"):
	    cur.execute("SELECT status, comment, location FROM sensors WHERE name=\'"+moteID+"\'")
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
            cur.execute("UPDATE sensors SET status=1, comment=\'" + request.json["comment"] + "\', location=\'" + request.json["location"] + "\'  WHERE name=\'"+moteID+"\'")
            cur.execute("SELECT status, comment  FROM sensors WHERE name=\'"+moteID+"\'")
            resp = cur.fetchone()
            cur.execute("INSERT INTO statuschange(newstatus,comment) VALUES ('on','"+request.json["comment"]+"\')")
        if (request.view_args["action"] == "off"):
            cur.execute("UPDATE sensors SET status=0, comment=\'"+ request.json["comment"] + "\', location=\'" + request.json["location"] + "\' WHERE name=\'"+moteID+"\'")
            cur.execute("SELECT status, comment  FROM sensors WHERE name=\'"+moteID+"\'")
            resp = cur.fetchone()
            cur.execute("INSERT INTO statuschange(newstatus,comment) VALUES ('off','"+request.json["comment"]+"\')")

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
    return json.dumps({"status":resp[0], "comment":resp[1],"location":resp[2]}) #str(strresponse) #Response(resp, content_type='text/plain; charset=utf-8')


@app.route('/meraki', methods=['POST'])
def meraki():



    # Create log of data
    f = open(os.path.join(config.UPLOAD_FOLDER, 'meraki.log'), "a")
    f.write(json.dumps(request.data) + "\n")
    f.close()

    requests.post('http://10.0.10.173:5000', json=json.loads(request.data),headers={'Content-type':'application/json'})
    return Response()

@app.route('/jdownes', methods=['POST'])
def jdownes():
    f = open(os.path.join(config.UPLOAD_FOLDER, 'jdownes.log'), "a")
    f.write(request.data + "\n")
    f.close()
    packet = json.loads(request.data)
    conn = MySQLConnection( host = '10.0.10.220',
                            database = 'ICP',
                            user = 'tran',
                            password = 'GreenX0123')
    curs = conn.cursor()

    # unit ID
    uID = "0x"+packet["DevEUI_uplink"]["DevAddr"] 
    f = open(os.path.join(config.UPLOAD_FOLDER, 'jdownes.log'), "a")
    f.write("uid= " +uID+ "\n")
    f.close()
    # time
    time = strftime('%Y-%m-%d %H:%M:%S')
    f = open(os.path.join(config.UPLOAD_FOLDER, 'jdownes.log'), "a")
    f.write("time= " +time+ "\n")
    f.close()
    # temp 
    tmpH = packet["DevEUI_uplink"]["payload_hex"]
    tmpH = tmpH[0:2]
    tmp = float(int(tmpH, 16))
    f = open(os.path.join(config.UPLOAD_FOLDER, 'jdownes.log'), "a")
    f.write("tmp= " +str(tmp)+ "\n")
    f.close()


    #humidity
    humH = packet["DevEUI_uplink"]["payload_hex"]
    humH = humH[2:]
    hum = float(int(humH, 16))
    f = open(os.path.join(config.UPLOAD_FOLDER, 'jdownes.log'), "a")
    f.write("hum= " +str(hum)+ "\n")
    f.close()


    add_read = ("CALL addRead(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

    data = (uID, time, 1, 1, tmp, hum, 0.0, 0.0, 0.0, 0.0)

    curs.execute(add_read, data)

    conn.commit()

    curs.close()
    conn.close()
    return Response()




if __name__ == '__main__':
    app.run(host='0.0.0.0')

