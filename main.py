import time
import API_XTB as xtb


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



def main():

    # enter your login credentials here
    userId = 12181707
    password = "xoh17643"

    # create & connect to RR socket
    client = xtb.APIClient()
    
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
    sclient = xtb.APIStreamClient(ssID=ssid)
    
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



