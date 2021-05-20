import json
import time
from API_XTB import *
from utils import *


def main():

    modal='real'
    bstreaming=False
    
    client = APIClient(mode=modal)
    loginResponse = client.execute(openFile('xtb_login.json'))
    
    if(loginResponse['status'] == False):
        print('Login failed. Error code: {0}'.format(loginResponse['errorCode']))
        return

    ssid = loginResponse['streamSessionId']
    
    if bstreaming:
        sclient = APIStreamClient(mode=modal,ssID=ssid)
      
    if bstreaming:
        #Streaming
        sclient.subscribe(openFile('streaming/getNews.json'))
        time.sleep(10)
        sclient.disconnect()
    else:    
        #No streaming
        client.execute(openFile('no_streaming/getNews.json'))
        time.sleep(3)
    
    client.disconnect()
    
    
    
    print('The time is done.')
    

    
if __name__ == "__main__":
    main()	



