import serial
from tracer import Tracer, TracerSerial #QueryCommand

#fake = None
# A sample response, to show what this demo does. Uncomment to use.
#fake = bytearray(b'\xEB\x90\xEB\x90\xEB\x90\x16\xA0\x18\xD2\x04\xD3\x04\x00\x00\x0E\x00\x53\x04\xA5\x05\x01\x00\x00\x1F\x00\x00\x00\x01\x33\x0A\x0A\x00\x9A\x38\x7F')

fake = bytearray(b'\xEB\x90\xEB\x90\xEB\x90\x16\xA0\x18\xCE\x04\xA4\x06\x00\x00\xE8\x03\x56\x04\xA0\x05\x01\x00\x00\x50\x00\x00\x00\x00\x37\xE8\x03\x00\x9A\x38\x7F')

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

if not fake:
    ser = serial.Serial('/dev/ttyAMA0', 9600, timeout = 1)
else:
    ser = FakePort(fake)

tracer = Tracer(0x16)
t_ser = TracerSerial(tracer, ser)
t_ser.send_command(0xA0)
result = t_ser.receive_result()

#print("result.data:\n", result.data)
#print(type(result.data))
#print("result:\n", result)
#print(type(result))
#data = str(result)
#print("str(result):\n", data)
#print(type(str(result)))

#for i in data:
#    print(i)
print ("Raw bytes: %s" % ", ".join(map(lambda a: "%0X" % (a), result.data)))
print
formatted = str(result).replace('{', '{\n')
formatted = formatted.replace('}', '\n}')
print (formatted.replace(', ', '\n'))
