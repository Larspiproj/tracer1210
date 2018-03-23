import logging
from logging.handlers import RotatingFileHandler
import os
from flask import Flask, render_template, url_for, jsonify
from flask_debugtoolbar import DebugToolbarExtension
#from time import sleep
from serial import Serial


import sys
sys.path.append('/home/pi/tracer1210/python')
from tracer import Tracer, TracerSerial

# Rest API
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key'
toolbar = DebugToolbarExtension(app)

if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/tracer.log', maxBytes=10240,
                                        backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.DEBUG)
    app.logger.info('Tracer startup')

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/solar', methods=['GET'])
def get_data():
    try:
        port = Serial('/dev/ttyAMA0', 9600, timeout=1)
        port.reset_input_buffer()
        port.reset_output_buffer()
        tracer = Tracer(0x16)
        t_ser = TracerSerial(tracer, port)
        t_ser.send_command(0xA0)
        #sleep(1)
        #data = t_ser.receive_result(36)
        data = t_ser.receive_result()
        port.close()
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
        port.reset_input_buffer()
        port.reset_output_buffer()
        return jsonify({'error': str(e)}), 503

@app.route('/load_on', methods=['GET'])
def load_on():
    try:
        port = Serial('/dev/ttyAMA0', 9600, timeout=1)
        tracer = Tracer(0x16)
        t_ser = TracerSerial(tracer, port)
        t_ser.send_command(0xAA, 0x01, 0x01)
        #data = t_ser.receive_result(13)
        data = t_ser.receive_result()
        port.close()
        load_state = data.load_state
        return render_template('load_on.html', load_state=load_state)        
    except (IndexError, IOError) as e:
        port.reset_input_buffer()
        port.reset_output_buffer()
        return jsonify({'error': str(e)}), 503

@app.route('/load_off', methods=['GET'])
def load_off():
    try:
        port = Serial('/dev/ttyAMA0', 9600, timeout=1)
        tracer = Tracer(0x16)
        t_ser = TracerSerial(tracer, port)
        t_ser.send_command(0xAA, 0x01, 0x00)
        #data = t_ser.receive_result(13)
        data = t_ser.receive_result()
        port.close()
        load_state = data.load_state
        return render_template('load_off.html', load_state=load_state) 
    except (IndexError, IOError) as e:
        port.reset_input_buffer()
        port.reset_output_buffer()
        return jsonify({'error': str(e)}), 503
