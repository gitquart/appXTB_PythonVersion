import json
import time
from API_XTB import *
from utils import *


def main():

    # enter your login credentials here
   

    # create & connect to RR socket
    client = APIClient(mode='real')
    
    # connect to RR socket, login
    loginResponse = client.execute(openFile('xtb_login.json'))
    

    # check if user logged in correctly
    if(loginResponse['status'] == False):
        print('Login failed. Error code: {0}'.format(loginResponse['errorCode']))
        return

    # get ssId from login response
    ssid = loginResponse['streamSessionId']
    

    #client.execute(openFile('cmd_no_streaming.json'))
    sclient = APIStreamClient(mode='real',ssID=ssid)
    
    
    sclient.subscribe(openFile('getTickPrices.json'))
    

    time.sleep(10)

    #sclient.unsubscribe(openFile('cmd_unsubscribe.json'))
    
    print('The time is done.')
    
    # gracefully close streaming socket
    #sclient.disconnect()
    
    # gracefully close RR socket
    client.disconnect()
    
    
if __name__ == "__main__":
    main()	



