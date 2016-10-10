import urllib.request
import time

while(1):
    response  = urllib.request.urlopen("http://cfo-864-as5g02/crt_print.png")
    image = response.read()
    print('status: '+str(response.status))
    ts_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print('images received @'+ts_str)
    f = open('test01_'+ ts_str + '.png', 'wb')
    f.write(image)
    f.close()
    time.sleep(30)

    
