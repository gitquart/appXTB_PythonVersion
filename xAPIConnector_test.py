import json
import socket
import logging
import time
import ssl
from threading import Thread

#Commands

json_login_cmd = {"command": "login",
	            "arguments": {
		                "userId": 12181707,
		                "password": "xoh17643",
		                "appName": ""
	                      }
	            }

json_NO_STREAMING_cmd={

    "command": "getSymbol",
	"arguments": {
		"symbol": "OIL"
	}
}

json_STREAMING_cmd={
	"command": "getTickPrices",
	"streamSessionId": "",
	"symbol": "EURUSD"
     }

json_STREAMING_cmd_2={
	"command": "getNews",
	"streamSessionId": ""
     }     


# set to true on debug environment only
DEBUG = True

#default connection properites
DEFAULT_XAPI_ADDRESS        = 'xapi.xtb.com'
DEFAULT_XAPI_PORT           = 5124
DEFUALT_XAPI_STREAMING_PORT = 5125

# wrapper name and version
WRAPPER_NAME    = 'python'
WRAPPER_VERSION = '2.5.0'

# API inter-command timeout (in ms)
API_SEND_TIMEOUT = 100

# max connection tries
API_MAX_CONN_TRIES = 3

# logger properties
logger = logging.getLogger("jsonSocket")
FORMAT = '[%(asctime)-15s][%(funcName)s:%(lineno)d] %(message)s'
logging.basicConfig(format=FORMAT)

if DEBUG:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.CRITICAL)


class TransactionSide(object):
    BUY = 0
    SELL = 1
    BUY_LIMIT = 2
    SELL_LIMIT = 3
    BUY_STOP = 4
    SELL_STOP = 5
    
class TransactionType(object):
    ORDER_OPEN = 0
    ORDER_CLOSE = 2
    ORDER_MODIFY = 3
    ORDER_DELETE = 4

#JsonSocket
class JsonSocket(object):
    def __init__(self, address, port, encrypt = False):
        self._ssl = encrypt 
        if self._ssl != True:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket = ssl.wrap_socket(sock)
        self.conn = self.socket
        self._timeout = None
        self._address = address
        self._port = port
        self._decoder = json.JSONDecoder()
        self._receivedData = ''

    def connect(self):
        for i in range(API_MAX_CONN_TRIES):
            try:
                self.socket.connect( (self.address, self.port) )
            except socket.error as msg:
                logger.error("SockThread Error: %s" % msg)
                time.sleep(0.25);
                continue
            logger.info("Socket connected")
            return True
        return False

    def _sendObj(self, obj):
        logger.info(obj)
        msg = json.dumps(obj)
        self._waitingSend(msg)

    def _waitingSend(self, msg):
        if self.socket:
            sent = 0
            msg = msg.encode('utf-8')
            while sent < len(msg):
                sent += self.socket.send(msg[sent:])
                logger.info('Sent: ' + str(msg))
                time.sleep(API_SEND_TIMEOUT/1000)

    def _read(self, bytesSize=4096):
        if not self.socket:
            raise RuntimeError("socket connection broken")
        while True:
            char = self.socket.recv(bytesSize).decode()
            self._receivedData += char
            try:
                (resp, size) = self._decoder.raw_decode(self._receivedData)
                if size == len(self._receivedData):
                    self._receivedData = ''
                    break
                elif size < len(self._receivedData):
                    self._receivedData = self._receivedData[size:].strip()
                    break
            except ValueError as e:
                continue
        logger.info('Received: ' + str(resp))
        return resp

    def _readObj(self):
        msg = self._read()
        return msg

    def close(self):
        logger.debug("Closing socket")
        self._closeSocket()
        if self.socket is not self.conn:
            logger.debug("Closing connection socket")
            self._closeConnection()

    def _closeSocket(self):
        self.socket.close()

    def _closeConnection(self):
        self.conn.close()

    def _get_timeout(self):
        return self._timeout

    def _set_timeout(self, timeout):
        self._timeout = timeout
        self.socket.settimeout(timeout)

    def _get_address(self):
        return self._address

    def _set_address(self, address):
        pass

    def _get_port(self):
        return self._port

    def _set_port(self, port):
        pass

    def _get_encrypt(self):
        return self._ssl

    def _set_encrypt(self, encrypt):
        pass

    timeout = property(_get_timeout, _set_timeout, doc='Get/set the socket timeout')
    address = property(_get_address, _set_address, doc='read only property socket address')
    port = property(_get_port, _set_port, doc='read only property socket port')
    encrypt = property(_get_encrypt, _set_encrypt, doc='read only property socket port')

#Fin JsonSocket    

#Inicio APIClient
class APIClient(JsonSocket):
    def __init__(self, address=DEFAULT_XAPI_ADDRESS, port=DEFAULT_XAPI_PORT, encrypt=True):
        super(APIClient, self).__init__(address, port, encrypt)
        if(not self.connect()):
            raise Exception("Cannot connect to " + address + ":" + str(port) + " after " + str(API_MAX_CONN_TRIES) + " retries")

    def execute(self, dictionary):
        self._sendObj(dictionary)
        return self._readObj()    

    def disconnect(self):
        self.close()
        

#Fin APIClient

#Inicio APIStreamClient
class APIStreamClient(JsonSocket):
    def __init__(self, address=DEFAULT_XAPI_ADDRESS, port=DEFUALT_XAPI_STREAMING_PORT, encrypt=True,ssID=None):
        super(APIStreamClient, self).__init__(address, port, encrypt)

        self._ssid=ssID
        
        if(not self.connect()):
            raise Exception("Cannot connect to streaming on " + address + ":" + str(port) + " after " + str(API_MAX_CONN_TRIES) + " retries")

        self._running = True
        self._t = Thread(target=self._readStream, args=())
        self._t.setDaemon(True)
        self._t.start()

    def _readStream(self):
        while (self._running):
                msg = self._readObj()
                logger.info("Stream received: " + str(msg))
               
    def disconnect(self):
        self._running = False
        self._t.join()
        self.close()

    def execute(self, dictionary):
        self._sendObj(dictionary)

    #Subscribe method will be always for Streaming, then an Streaming ID is required
    def subscribe(self,command):
        #command must be a dictionary already, not string.
        command['streamSessionId']=self._ssid
        #command=json.dumps(command)
        self.execute(command)
        
    def unsubscribe(self,command):
        self.execute(command)
        
   
# Fin APIStreamClient


def printJSONtoFile(fileName,content):
    print('Printing JSON...')
    with open(fileName, 'w') as outfile:
        json.dump(content, outfile)


    

def main():

    # enter your login credentials here
    userId = 12181707
    password = "xoh17643"

    # create & connect to RR socket
    client = APIClient()
    
    # connect to RR socket, login
    loginResponse = client.execute(json_login_cmd)
    

    # check if user logged in correctly
    if(loginResponse['status'] == False):
        print('Login failed. Error code: {0}'.format(loginResponse['errorCode']))
        return

    # get ssId from login response
    ssid = loginResponse['streamSessionId']
    
    
    #resp = client.execute(json_NO_STREAMING_cmd)
    #print(resp)
    
    # create & connect to Streaming socket with given ssID
    # and functions for processing ticks, trades, profit and tradeStatus
    sclient = APIStreamClient(ssID=ssid)
    
    # subscribe for trades
    sclient.subscribe(json_STREAMING_cmd)


    


    # this is an example, make it run for 5 seconds
    time.sleep(10)
    
    # gracefully close streaming socket
    sclient.disconnect()
    
    # gracefully close RR socket
    client.disconnect()
    
    
if __name__ == "__main__":
    main()	



