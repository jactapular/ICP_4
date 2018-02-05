# Import library and create instance of REST client.
from Adafruit_IO import Client

@app.route('/ikareem', methods=['POST'])
def ikareem():

packet = json.loads(request.data)

#connect to a adafruit
aio = Client('d361959719e34664a85846131b80457c')

ambtemp = packet["DevEUI_uplink"]["payload_hex"]
#must multiply data by 100 on arduino end
    val = float(int(ambtemp, 16))/100

# Add the value 98.6 to the feed 'Temperature'.
aio.send('temp-readings.ambient-air-temp', val)