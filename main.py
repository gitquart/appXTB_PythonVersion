import json
import time
from API_XTB import *
from utils import *


def main():

    # enter your login credentials here
   

    # create & connect to RR socket
    client = APIClient()
    
    # connect to RR socket, login
    loginResponse = client.execute(openFile('xtb_login.json'))
    

    # check if user logged in correctly
    if(loginResponse['status'] == False):
        print('Login failed. Error code: {0}'.format(loginResponse['errorCode']))
        return

    # get ssId from login response
    ssid = loginResponse['streamSessionId']
    
    
    # create & connect to Streaming socket with given ssID
    # and functions for processing ticks, trades, profit and tradeStatus
    sclient = APIStreamClient(ssID=ssid)
    
    # subscribe for trades
    sclient.subscribe(openFile('cmd_streaming.json'))

    time.sleep(5)
    print('The time is done.')

    #sclient.unsubscribe(openFile('cmd_unsubscribe.json'))

    
    
    # gracefully close streaming socket
    sclient.disconnect()
    
    # gracefully close RR socket
    client.disconnect()
    
    
if __name__ == "__main__":
    main()	



