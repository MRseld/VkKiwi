import settings
import requests
import json 
from vkObjects import convestationsObject
from vkObjects import vkapierrorObject
import time
from collections import namedtuple
def VkApiCallMethod(method:str,params:list):
    _params=""
    for i in params:
        print(i)
        _params=_params+i+"&"

    requestsUrl=settings.api_domain_name+method+"?"+_params+"access_token="+settings.access_token+"&v="+settings.api_version
    print(requestsUrl)
    response= requests.get(requestsUrl).text

    error=vkapierrorObject.vkapi_error_object_from_dict(json.loads(response)).error

    if error ==None:
        return(response)
    elif error.error_code==6:
        time.sleep(1)
    
        return VkApiCallMethod(method,params)
    else: raise ApiException(error)

class ApiException(Exception):
    def __init__(self,error:vkapierrorObject.Error):
        self._Error=error  
    def get_code(self):
         return self._Error.error_code
    def get_str_code(self):
        return str(self._Error.error_code)
    def get_msg(self):
        return self._Error.error_msg
    def get_requests_params(self):
        return self._Error.request_params
    
class Messages():
    def get(count,offset,extended):
        try:
            z=VkApiCallMethod("messages.getConversations",["extended="+str(extended), "count="+str(count),"offset="+str(offset)])
            return convestationsObject.convestation_from_dict(json.loads(z))
        except ApiException as e:
           raise e
        
        
       
