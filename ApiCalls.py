import settings
import requests
import json 


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
    


    error=None
  
    return response


    
class Messages():
    def get(self,count,offset,extended):
      
        return json.loads(VkApiCallMethod("messages.getConversations",["extended="+str(extended), "count="+str(count),"offset="+str(offset)]))
           
    def getHistory(self,count,offset,peer_id,rev, extended):
        return json.loads( VkApiCallMethod("messages.getHistory",["count="+str(count),"offset="+str(offset),"peer_id="+str(peer_id),
        "rev="+str(rev),"extended="+str(extended)]) )

        

      

class LongPoll():
    _longpolldata=None
  
    _server=None
    _key=None
    _ts=None
    _mode=None
    def getLongPollServer(self):
      
          longpoll=json.loads(VkApiCallMethod("messages.getLongPollServer",["lp_version=3"]) )
          self.setKey(longpoll["response"]["key"])
          self.setTs(longpoll["response"]["ts"])
          self.setServer(longpoll["response"]["server"]) 
     
          
    def RequestServer(self):
        request= requests.get( "https://"+self.getServer()+"?act=a_check&key="+str(self.getKey())+"&ts="+str(self.getTs())+"&wait=25&mode="+str(self.getMode())+"&version=3").text
        self._longpolldata=json.loads(request)
        self.setTs(self._longpolldata["ts"])
  
    def getLongPolldata(self):
        return self._longpolldata

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
    
    
        


        
        
       
