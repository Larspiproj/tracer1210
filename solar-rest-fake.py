from flask import Flask, render_template, url_for, jsonify
from time import sleep
from serial import Serial

import sys
sys.path.append('/home/pi/tracer1210/python')
from tracer import Tracer, TracerSerial, QueryCommand

# default fake
#fake = bytearray(b'\xEB\x90\xEB\x90\xEB\x90\x00\xA0\x18\xD2\x04\xD3\x04 \
#    \x00\x00\x0E\x00\x53\x04\xA5\x05\x01\x00\x00\x1F\x00\x00\x00\x01\x33 \
#    \x0A\x00\x00\x99\x5B\x7F')

fake = bytearray(b'\xEB\x90\xEB\x90\xEB\x90\x00\xA0\x1F\xD2\x04\xD3\x04 \
    \x00\x00\x0E\x00\x53\x04\xA5\x05\x01\x00\x00\x1F\x00\x00\x00\x01\x33 \
    \x0A\x00\x00\x99\x5B\x7F')

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
#port = FakePort(fake)
#port.flushInput()
#port.flushOutput()
#tracer = Tracer(0x16)
#t_ser = TracerSerial(tracer, port)
#query = QueryCommand()


# Rest API
app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
        return render_template('index.html')

@app.route('/solar', methods=['GET'])
def get_data():
    try:
        #port = Serial('/dev/ttyAMA0', 9600, timeout=1)
        port = FakePort(fake)
        #port.flushInput()
        #port.flushOutput()
        tracer = Tracer(0x16)
        t_ser = TracerSerial(tracer, port)
        query = QueryCommand()
        t_ser.send_command(query)
        data = t_ser.receive_result()
        # operating parameters
        batt_voltage =  data.batt_voltage
        batt_full_voltage = data.batt_full_voltage
        batt_overdischarge_voltage = data.batt_overdischarge_voltage
        batt_temp = data.batt_temp
        pv_voltage = data.pv_voltage
        charge_current = data.charge_current
        load_on = data.load_on
        load_amps = data.load_amps
        load_overload = data.load_overload
        load_short = data.load_short
        batt_overdischarge = data.batt_overdischarge
        batt_full = data.batt_full
        batt_overload = data.batt_overload
        batt_charging = data.batt_charging


        return render_template('data.html',
                         batt_voltage=batt_voltage,
                         batt_full_voltage=batt_full_voltage,
                         batt_overdischarge_voltage=batt_overdischarge_voltage,
                         batt_temp=batt_temp,
                         pv_voltage=pv_voltage,
                         charge_current=charge_current,
                         load_on=load_on,
                         load_amps=load_amps,
                         load_overload=load_overload,
                         load_short=load_short,
                         batt_overdischarge=batt_overdischarge,
                         batt_full=batt_full,
                         batt_overload=batt_overload,
                         batt_charging=batt_charging)
        '''
        return jsonify(batt_voltage=data.batt_voltage,
                       pv_voltage=data.pv_voltage,
                       charge_current=data.charge_current,
                       load_amps=data.load_amps)
        '''

    except (IndexError, IOError) as e:
        #port.flushInput()
        #port.flushOutput()
        return jsonify({'error': str(e)}), 503
        #return {'error': str(e)}, 503
        #return str(e)

if (__name__) == ('__main__'):

    try:
        app.run()

    except KeyboardInterrupt:
        print ("\nCtrl-C pressed.  Closing serial port and exiting...")
    finally:
        port.close()
        pass
