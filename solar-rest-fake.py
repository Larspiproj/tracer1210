from flask import Flask, jsonify
from time import sleep
from serial import Serial

import sys
sys.path.append('/home/pi/tracer1210/python')
from tracer import Tracer, TracerSerial, QueryCommand

fake = bytearray(b'\xEB\x90\xEB\x90\xEB\x90\x00\xA0\x18\xD2\x04\xD3\x04\x00\x00\x0E\x00\x53\x04\xA5\x05\x01\x00\x00\x1F\x00\x00\x00\x01\x33\x0A\x00\x00\x99\x5B\x7F')

class FakePort(object):
    def __init__(self, data):
        self.data = data
    read_idx = 0
    def read(self, count=1):
        result = self.data[self.read_idx:self.read_idx+count]
        self.read_idx += count
        return result
    def write(self, data):
        return len(data)

#port = Serial('/dev/ttyAMA0', 9600, timeout=1)
port = FakePort(fake)
#port.flushInput()
#port.flushOutput()
tracer = Tracer(0x16)
t_ser = TracerSerial(tracer, port)
query = QueryCommand()


# Rest API
app = Flask(__name__)

@app.route('/solar', methods=['GET'])
def get_data():
    try:
        t_ser.send_command(query)
        data = t_ser.receive_result()

        return jsonify(batt_voltage=data.batt_voltage,
                       pv_voltage=data.pv_voltage,
                       charge_current=data.charge_current,
                       load_amps=data.load_amps)

    except (IndexError, IOError) as e:
        #port.flushInput()
        #port.flushOutput()
        return jsonify({'error': str(e)}), 503
        #return str(e)

if (__name__) == ('__main__'):

    try:
        app.run()

    except KeyboardInterrupt:
        print ("\nCtrl-C pressed.  Closing serial port and exiting...")
    finally:
        #port.close()
        pass
