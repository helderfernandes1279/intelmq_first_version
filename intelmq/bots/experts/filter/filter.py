import json
from intelmq.lib.bot import Bot, sys

           
class FilterExpertBot(Bot):
    
    def init(self):
	filereader=open(self.parameters.rulesfile,"r")
	self.filterdata=json.loads(filereader.read())
	filereader.close()

	
    def process(self):
        event = self.receive_message()

        if event:
	   for rule in self.filterdata: 
	     
	      keys=rule.keys()
              rulematch=True

	      for key in keys:
            	  eventvalue = event.value(key)
	    
	          if eventvalue:
		     if not rule[key]==eventvalue:
			rulematch=False
			break;		    	    
                  else:
		    rulematch=False
		    break;  
	     
	      if rulematch==True:
		  self.send_message(event)
                  self.logger.info("Match")
		  break; 	
		                      
        self.acknowledge_message()


if __name__ == "__main__":
    bot = FilterExpertBot(sys.argv[1])
    bot.start()
