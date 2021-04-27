"""
main.py
The xAPIConnector.py works well but it's a wrapper, so this main.py
file will aim to send any API command described in http://developers.xstore.pro/documentation/#introduction
"""

import socket
import json

DEFAULT_XAPI_ADDRESS= 'xapi.xtb.com'
DEFUALT_XAPI_STREAMING_PORT = 5125
DEFAULT_XAPI_PORT= 5124


url=''
json_command = {"command": "login",
	            "arguments": {
		                "userId": "12181707",
		                "password": "xoh17643",
                        "appId": "",
		                "appName": ""
	                      }
	            }




def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((DEFAULT_XAPI_ADDRESS, DEFUALT_XAPI_STREAMING_PORT))
	api_command= json.dumps(json_command)
	print('...')
    
   







if __name__ == "__main__":
    main()	
