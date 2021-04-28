"""
main.py
The xAPIConnector.py works well but it's a wrapper, so this main.py
file will aim to send any API command described in http://developers.xstore.pro/documentation/#introduction
"""

import socket
import json
import time
import ssl

DEFAULT_XAPI_ADDRESS= 'xapi.xtb.com'
DEFAULT_XAPI_STREAMING_PORT = 5125
DEFAULT_XAPI_PORT= 5124
API_SEND_TIMEOUT = 100

json_login_cmd = {"command": "login",
	            "arguments": {
		                "userId": 12181707,
		                "password": "xoh17643",
		                "appName": ""
	                      }
	            }

json_NO_STREAMING_cmd={

    "command": "getCalendar"
}

json_STREAMING_cmd={

    
	"command": "getBalance",
	"streamSessionId": ""

}



def getSocket(port):
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((DEFAULT_XAPI_ADDRESS,port))
    my_socket=ssl.wrap_socket(my_socket)
    return my_socket


def sendXTBCommand(my_socket,api_command,op,ssid=''):
    '''
    Method: sendXTBCommand
    Description: Sends the request to XTB API
    params: 
        op=0 is No streaming, 1 is streaming
        ssid: current Stram Session ID
    '''
    api_command= json.dumps(api_command)
    if my_socket:
        sent = 0
        if op==1:
            data = json.loads(api_command)
            data['streamSessionId']=ssid
            api_command=json.dumps(data)
            
        api_command_encoded = api_command.encode('utf-8')
        while sent < len(api_command_encoded):
            sent += my_socket.send(api_command_encoded[sent:])
            time.sleep(API_SEND_TIMEOUT/1000)
        if sent>0:
            return True   

def receiveXTBAnswer(my_socket):
    receivedData=''
    decoder = json.JSONDecoder()
    if not my_socket:
        raise RuntimeError("socket connection broken")
    while True:
        char = my_socket.recv(4096).decode()
        receivedData += char
        try:
            (resp, size) = decoder.raw_decode(receivedData)
            if size == len(receivedData):
                receivedData = ''
                break
            elif size < len(receivedData):
                receivedData = receivedData[size:].strip()
                break
        except ValueError as e:
            continue
    return resp
    


#getStreamSessionId gets the StreamingSessionID
def getStreamSessionId(ssl_socket):
    bRes=sendXTBCommand(ssl_socket,json_login_cmd,0)
    res=''
    try:
        if bRes:
            respXTB=receiveXTBAnswer(ssl_socket)
            res=respXTB['streamSessionId']
            print('The ID Stream Session is ',res)
    except Exception as e:
        res=e
    return res 

def printJSONtoFile(fileName,content):
    print('Printing JSON...')
    with open(fileName, 'w') as outfile:
        json.dump(content, outfile)



def main():
    #Get socket (and it's open already)
    
    ssl_socket_no_streaming=getSocket(DEFAULT_XAPI_PORT)
    ssid=getStreamSessionId(ssl_socket_no_streaming)
    
    #NO STREAMING
    #Example of how to call a NO STREAMING method (Retrieving trading data : http://developers.xstore.pro/documentation/#retrieving-trading-data)
    """
    res=sendXTBCommand(ssl_socket_no_streaming,json_NO_STREAMING_cmd)
    if res:
        xtbRes=receiveXTBAnswer(ssl_socket_no_streaming)
        printJSONtoFile('C:\\Users\\1098350515\\Desktop\\getCalendar.json',xtbRes)
    """    

    #STREAMING
    ssl_socket_streaming=getSocket(DEFAULT_XAPI_STREAMING_PORT)  
    res=sendXTBCommand(ssl_socket_streaming,json_STREAMING_cmd,1,ssid)
    if res:
        xtbRes=receiveXTBAnswer(ssl_socket_streaming)
        print(xtbRes)



    ssl_socket_no_streaming.close()  
    ssl_socket_streaming.close()  

    

if __name__ == "__main__":
    main()	
