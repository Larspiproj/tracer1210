from flask import Flask, jsonify
from time import sleep
from serial import Serial

import sys
sys.path.append('/home/pi/tracer1210/python')
from tracer import Tracer, TracerSerial, QueryCommand

port = Serial('/dev/ttyAMA0', 9600, timeout=1)
port.flushInput()
port.flushOutput()
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
                       load_amps=data.load_amps,
                       batt_full_voltage=data.batt_full_voltage,
                       batt_charging=data.batt_charging,
                       batt_temp=data.batt_temp)

    except (IndexError, IOError) as e:
        port.flushInput()
        port.flushOutput()
        return jsonify({'error': str(e)}), 503

if (__name__) == ('__main__'):
    try:
        app.run()

    except KeyboardInterrupt:
        print ("\nCtrl-C pressed.  Closing serial port and exiting...")
    finally:
        port.close()
