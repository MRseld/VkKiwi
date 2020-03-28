import settings
import requests
import json 
from vkObjects import convestationsObject
from vkObjects import vkapierrorObject
from vkObjects import longpollObject
from vkObjects import longpolldataobject

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
    def get(self,count,offset,extended):
        try:
            z=VkApiCallMethod("messages.getConversations",["extended="+str(extended), "count="+str(count),"offset="+str(offset)])
            return convestationsObject.convestation_from_dict(json.loads(z))
        except ApiException as e:
           raise e

class LongPoll():
    _longpolldataText=None
    _longpollDataObject:longpolldataobject.LongpolldataObject=None
    _server=None
    _key=None
    _ts=None
    _mode=None
    def getLongPollServer(self):
        try:
          longpoll=longpollObject.longpoll_from_dict(json.loads( VkApiCallMethod("messages.getLongPollServer",["lp_version=3"])))    
          self.setKey(longpoll.response.key)
          self.setTs(longpoll.response.ts)
          self.setServer(longpoll.response.server) 
        except ApiException as e:
           raise e
        pass
          
    def RequestServer(self):
        request= requests.get( "https://"+self.getServer()+"?act=a_check&key="+str(self.getKey())+"&ts="+str(self.getTs())+"&wait=25&mode="+str(self.getMode())+"&version=3").text
        self._longpolldataText=request
        self._longpollDataObject= longpolldataobject.longpolldata_object_from_dict(json.loads(request))
        self.setTs(self._longpollDataObject.ts)
  
    def getLongPolldataObject(self):
        return self._longpollDataObject  

    def update(self):
        pass
    
    def setKey(self,value):
        self._key=value
    def setTs(self,value):
        self._ts=value
    def setServer(self,value):
        self._server=value
    def setMode(self,value):
        self._mode=value
    
    def getKey(self):
        return self._key
    def getTs(self):
         return self._ts
    def getServer(self):
        return self._server
    def getMode(self):
        return self._mode
    
    
        


        
        
       
