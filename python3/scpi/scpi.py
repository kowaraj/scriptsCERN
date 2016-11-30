
import socket

class Instr():

    def __init__(self, host, port=5025):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

    def send(self, cmd_str):
        send_str = cmd_str + ';\n'
        send_b = send_str.encode('utf-8')
        self.sock.sendall(send_b)

    def receive(self):
        ret = self.sock.recv(1024)
        print("ret = ", ret)
        return ret

    def meas_freq(self):
        self.send('*RST')
        self.send('MEAS:FREQ? 200E6, 0.1, (@3)')
        self.receive()

    def meas_freq_10(self):
        self.send('*RST')
        self.send('CONF:FREQ 200E6, 0.1, (@3)')
        self.send('SAMP:COUN 10')
        self.send('READ?')
        self.receive()

    def conf(self):
        self.send('CONF:FREQ 200.0E6, (@3)')
        self.send('TRIG:SOUR EXT')
        self.send('TRIG:SLOP POS')
        self.send('TRIG:COUN 1')
        self.send('SAMP:COUN 5')
        self.send('SENS:FREQ:GATE:TIME 0.005')
        self.send('SENS:FREQ:GATE:SOUR TIME')
        self.send('INIT')
        
    def meas_freq_now(self):
        print(__name__)
        self.send('*RST')
        self.send('CONF:FREQ 200.0E6, (@3)')
        self.send('TRIG:SOUR EXT')
        self.send('TRIG:SLOP NEG')
        self.send('TRIG:COUN 1')
        self.send('SAMP:COUN 1')
        self.send('SENS:FREQ:GATE:TIME 0.005')
        self.send('SENS:FREQ:GATE:SOUR TIME')
        self.send('INIT')
        self.send('READ?')
        self.receive()


    def meas01(self):
        self.send('CONF:FREQ (@1)')
        # self.send('TRIG:SOUR EXT')
        # self.send('TRIG:SLOP NEG')
        # self.send('TRIG:COUN 1')
        # self.send('SAMP:COUN 1')
        self.send('SENS:FREQ:GATE:TIME 0.005')
        self.send('SENS:FREQ:GATE:SOUR TIME')
        self.send('INIT')
        self.send('READ?')
        self.receive()

    def meas06(self):
        self.send('*RST')
        self.send('meas:freq? 200e6, 0.01, (@3)')
        self.receive()
        
