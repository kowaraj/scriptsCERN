#!/user/bdisoft/operational/bin/Python/PRO/bin/python


# Echo server program
# import socket

# HOST = 'cfo-ba3-ac6g02'
# PORT = 5025 
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.connect((HOST, PORT))
#     s.sendall(b'*idn?;\n')
#     ret = s.recv(1024)
#     print("ret = ", ret)


import scpi

instr = scpi.Instr('cfo-ba3-ac6g02')
instr.send('*idn?')
instr.receive()


#instr.meas_freq()
# instr.conf()
# instr.receive()
instr.meas06()
