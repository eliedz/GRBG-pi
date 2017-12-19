from gps3 import gps3
import json
from aiocoap import *

API_ENDPOINT = "192.168.43.8:5000"
gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gps_socket.connect()
gps_socket.watch()
for new_data in gps_socket:
    if new_data:
        data_stream.unpack(new_data)
        if data_stream.TPV['alt'] != 'n/a':
            longitude = data_stream.TPV['lon']
            latitude = data_stream.TPV['lat']
            print latitude
            print longitude
            break
while True:
    companyID = raw_input("Enter Company ID: ")
    piID = raw_input("Enter pi ID: ")
    binDepth = raw_input("Enter Bin Depth: ")
    binVolume = raw_input("Enter Bin Volume: ")
    data = {'company_id':companyID,'req_id':piID,'longitude':longitude,'latitude':latitude,'volume':binVolume}
    request = Message(code=PUT, payload=data)
    request.opt.uri_host = API_ENDPOINT
    request.opt.uri_path = "register"
    response = await context.request(request).response
    response = json.loads(r.text)
    if response['status_code'] == 200:
        with open('binInfo.txt', 'w+') as the_file:
            the_file.write(companyID + "\n")
            the_file.write(piID + "\n")
            the_file.write(binDepth + "\n")
            the_file.write(binVolume + "\n")
        break
    print response['status_code']
    print response['message']
