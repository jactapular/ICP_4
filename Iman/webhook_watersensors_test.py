# Import library and create instance of REST client.
from Adafruit_IO import Client

    
aio = Client('d361959719e34664a85846131b80457c')

# Add the value 98.6 to the feed 'Temperature'.
aio.send('temp-readings.ambient-air-temp', 25.0)
aio.send('temp-readings.ambient-air-temp', 25.0)
aio.send('temp-readings.ambient-air-temp', 25.0)
aio.send('temp-readings.ambient-air-temp', 25.0)
aio.send('temp-readings.ambient-air-temp', 25.0)
aio.send('temp-readings.ambient-air-temp', 25.0)
aio.send('temp-readings.ambient-air-temp', 25.0)