import json,ipaddress
from intelmq.lib.bot import Bot, sys

           
class ConstituencyExpertBot(Bot):
    
    def process(self):
        event = self.receive_message()
        contacts=self.parameters.database
        if event:
	    keys_ip=["source_%s", "destination_%s"]
            for key in keys_ip:
            	ip = event.value(key % "ip")
	    
		if ip:		    	
		   entity=self.get_constituency(contacts,ip) 
		   if entity:
		      event.add(key % "entity", entity['entity_id'])
		   else:
		      event.add(key % "entity", "external")    
		      
		               
            self.send_message(event)
        self.acknowledge_message()
    



    def get_constituency(self,fullpath_to_contacts,ip):
    	check_ip=ipaddress.ip_address(ip)	
    	fp=open(fullpath_to_contacts,'r')
    	data=json.load(fp)
    	constituency_id=''
    	netlist=[]
    	entity={}
    	for item in data:
    	 for subnet in item['cidrs']:	   
    	    if check_ip in ipaddress.ip_network(subnet, strict=False):
	      if not check_ip in ipaddress.ip_network('194.210.238.64/26',strict=False):
	        if not check_ip in ipaddress.ip_network('194.210.238.128/26',strict=False): 
	          info={}
	          info['entity_id']=item['_id']
	          info['network']=subnet
	          netlist.append(info)
    
   	maxprefix=0
	  
    	for item in netlist:
	    prefix=ipaddress.ip_network(item['network'],strict=False).prefixlen        
	
	    if maxprefix < prefix:
	       maxprefix=prefix 
               entity=item
  
        return entity


if __name__ == "__main__":
    bot = ConstituencyExpertBot(sys.argv[1])
    bot.start()
