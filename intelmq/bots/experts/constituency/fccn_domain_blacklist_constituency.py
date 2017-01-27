import json,ipaddress,ast
from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Event
from intelmq.bots import utils

           
class FCCN_domain_Blacklist_ConstituencyExpertBot(Bot):
    
    def process(self):
        event = self.receive_message()
	domainslist=ast.literal_eval(event)
        contacts=self.parameters.database
        if domainslist:
	  for domain in domainslist:
	   if domain['domain'].find('.pt',len(domain['domain'])-3,len(domain['domain']))> -1:
  	    ip = utils.get_ip_from_domain_name(domain['domain'])
	    domain['ip_address']=ip
	    if ip: 		    	
	     entity=self.get_constituency(contacts,ip)
	      
	     if entity and entity['entity_id'].find('FCCN')!=-1:
	        domain['entity']=entity['entity_id']
	     else:
	        domain['entity']="external"
		      
		               
             self.send_message(Event(domain))
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
                if not check_ip in ipaddress.ip_network('194.210.238.0/26',strict=False):   
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
    bot = FCCN_domain_Blacklist_ConstituencyExpertBot(sys.argv[1])
    bot.start()
