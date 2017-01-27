import json
from intelmq.lib.bot import Bot, sys

           
class ExclusionsExpertBot(Bot):
    
   


	
    def process(self):
        event = self.receive_message()
        filereader=open(self.parameters.exclusionsfile,"r")
	exclusionsdata=json.loads(filereader.read())
	filereader.close()
        if event:
	   event.add('Excluded','N')
	   for rule in exclusionsdata: 
	     
	      keys=rule.keys()
              rulematch=True

	      for key in keys:
		  if key.lower()!='exclusion_description' and key.lower()!='id':
            	     eventvalue = event.value(key)
	    
	             if eventvalue:
		        if not rule[key].lower()==eventvalue.lower():
			   rulematch=False
			   break;		    	    
                     else:
		       rulematch=False
		       break;  
	     
	      if rulematch==True:
		  event.clear('Excluded')
		  event.add('Excluded','Y')
		  if 'exclusion_description' in rule.keys():
	      	     event.add('Exclusion_description',rule['exclusion_description'])	 
		     break;
		  else:
		     break;
	   self.send_message(event) 			                      
           self.acknowledge_message()


if __name__ == "__main__":
    bot = ExclusionsExpertBot(sys.argv[1])
    bot.start()
