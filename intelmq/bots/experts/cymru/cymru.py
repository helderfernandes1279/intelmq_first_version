import json,threading
from copy import deepcopy
from intelmq.lib.bot import Bot, sys
from intelmq.lib.cache import Cache
from intelmq.bots import utils
from intelmq.bots.experts.cymru.lib import Cymru

MINIMUM_BGP_PREFIX_IPV4 = 24
MINIMUM_BGP_PREFIX_IPV6 = 128 # FIXME

class CymruExpertBot(Bot):
    
    def init(self):
        self.cache = Cache(
                            self.parameters.redis_cache_host,
                            self.parameters.redis_cache_port,
                            self.parameters.redis_cache_db,
                            self.parameters.redis_cache_ttl
                          )

	
	self.threads = []
	self.thread=None
    	self.threadLock = None
    	self.threadcount=0
    	self.maxconnections = 5
    	self.pool_sema = threading.BoundedSemaphore(value=self.maxconnections)	


    
    def process(self):
        self.pool_sema.acquire()
        event = self.receive_message()
	if event:
           self.thread=botthread(self.send_message,event,self.logger,self.cache) 
           self.thread.start()	
	   
        self.pool_sema.release()  
        self.acknowledge_message()




class botthread(threading.Thread):
    def __init__(self, sendmsg_obj,eventobj,log,cache):
        threading.Thread.__init__(self)
        self.send_message = sendmsg_obj
        self.event=deepcopy(eventobj)
        self.logger=log
	self.cache=cache
  
    def run(self):
	
        
        keys = ["source_%s", "destination_%s"]
        
        for key in keys:
            ip = self.event.value(key % "ip")
            
            if not ip:
                self.send_message(self.event)
                return

            elif utils.is_ipv4(ip):
                ip_version = 4
                ip_integer = utils.ip_to_int(ip)
                cache_key = bin(ip_integer)[2 : MINIMUM_BGP_PREFIX_IPV4 + 2]

            elif utils.is_ipv6(ip):
                ip_version = 6
                ip_integer = utils.ip_to_int(ip)
                cache_key = bin(ip_integer)[2 : MINIMUM_BGP_PREFIX_IPV6 + 2]

            else:
                self.send_message(self.event)
                return


            result_json = self.cache.get(cache_key)

            if result_json:
                result = json.loads(result_json)
            else:
                result = Cymru.query(ip, ip_version)
                result_json = json.dumps(result)
                self.cache.set(cache_key, result_json)
            
            if "asn" in result:
                self.event.clear(key % 'asn')
                self.event.add(key % 'asn',        result['asn'])
                
            if "bgp_prefix" in result:
                self.event.clear(key % 'bgp_prefix')
                self.event.add(key % 'bgp_prefix', result['bgp_prefix'])
                
            if "registry" in result:
                self.event.clear(key % 'registry')
                self.event.add(key % 'registry',   result['registry'])
                
            if "allocated" in result:
                self.event.clear(key % 'allocated')
                self.event.add(key % 'allocated',  result['allocated'])
                
            if "as_name" in result:
                self.event.clear(key % 'as_name')
                self.event.add(key % 'as_name',    result['as_name'])
                
            if "cc" in result:
                self.event.clear(key % 'cymru_cc')
                self.event.add(key % 'cymru_cc',   result['cc'])

        self.send_message(event)
        
        
if __name__ == "__main__":
    bot = CymruExpertBot(sys.argv[1])
    bot.start()
