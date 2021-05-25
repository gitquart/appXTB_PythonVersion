import json
import time
from API_XTB import *
from utils import *


def main():

    modal='real'
    bstreaming=False
    userId=''
    pwd=''
    if modal=='demo':
        userId=12246157
        pwd='judith123'
    else:
        userId=1832076
        pwd='Quart2020'

    loginJson=openFile('xtb_login.json')
    loginJson['arguments']['userId']=userId
    loginJson['arguments']['password']=pwd
    client = APIClient(mode=modal)
    loginResponse = client.execute(loginJson)
    
    if(loginResponse['status'] == False):
        print('Login failed. Error code: {0}'.format(loginResponse['errorCode']))
        return

    ssid = loginResponse['streamSessionId']
    
    if bstreaming:
        sclient = APIStreamClient(mode=modal,ssID=ssid)
      
    if bstreaming:
        #Streaming
        sclient.subscribe(openFile('streaming/getTrades.json'))
        secs=15
        print('Holding :',str(secs),' secs.')
        time.sleep(secs)
        sclient.disconnect()
    else:    
        #No streaming
        client.execute(openFile('no_streaming/getTickPrices.json'))
        secs=3
        print('Holding :',str(secs),' secs.')
        time.sleep(secs)
    
    client.disconnect()
    
    
    
    print('The time is done.')
    

    
if __name__ == "__main__":
    main()	



