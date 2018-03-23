from flask import Flask, render_template, url_for, jsonify
#from time import sleep
from serial import Serial

import sys
sys.path.append('/home/pi/tracer1210/python')
from tracer import Tracer, TracerSerial


# default fake
#fake = bytearray(b'\xEB\x90\xEB\x90\xEB\x90\x00\xA0\x18\xD2\x04\xD3\x04 \
#    \x00\x00\x0E\x00\x53\x04\xA5\x05\x01\x00\x00\x1F\x00\x00\x00\x01\x33 \
#    \x0A\x00\x00\x99\x5B\x7F')

fake = bytearray(b'\xEB\x90\xEB\x90\xEB\x90\x00\xA0\x18\xD2\x04\xD3\x04 \
    \x00\x00\x0E\x00\x53\x04\xA5\x05\x01\x00\x00\x1F\x00\x00\x00\x01\x33 \
    \x0A\x00\x00\x99\x5B\x7F')

fake_load_off = bytearray(b'\xEB\x90\xEB\x90\xEB\x90\x16\xAA\x01\x00\x99\x5B\x7F')
fake_load_on = bytearray(b'\xEB\x90\xEB\x90\xEB\x90\x16\xAA\x01\x01\x99\x5B\x7F')

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

# Rest API
app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/solar', methods=['GET'])
def get_data():
    try:
        port = FakePort(fake)
        tracer = Tracer(0x16)
        t_ser = TracerSerial(tracer, port)
        t_ser.send_command(0xA0)
        #data = t_ser.receive_result(36)
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

    except (IndexError, IOError) as e:
        return jsonify({'error': str(e)}), 503

@app.route('/load_on', methods=['GET'])
def load_on():
    try:
        port = FakePort(fake_load_on)
        tracer = Tracer(0x16)
        t_ser = TracerSerial(tracer, port)
        t_ser.send_command(0xAA, 0x01, 0x01)
        #data = t_ser.receive_result(13)
        data = t_ser.receive_result()
        load_state = data.load_state
        return render_template('load_on.html', load_state=load_state)        
    except (IndexError, IOError) as e:
        return jsonify({'error': str(e)}), 503

@app.route('/load_off', methods=['GET'])
def load_off():
    try:
        port = FakePort(fake_load_off)
        tracer = Tracer(0x16)
        t_ser = TracerSerial(tracer, port)
        t_ser.send_command(0xAA, 0x01, 0x00)
        #data = t_ser.receive_result(13)
        data = t_ser.receive_result()
        load_state = data.load_state
        return render_template('load_off.html', load_state=load_state) 
    except (IndexError, IOError) as e:
        return jsonify({'error': str(e)}), 503
