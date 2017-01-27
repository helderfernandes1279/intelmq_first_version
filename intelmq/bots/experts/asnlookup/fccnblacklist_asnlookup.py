import pyasn
from intelmq.lib.bot import Bot, sys

class fccnblacklist_ASNLookupExpertBot(Bot):

    def init(self):
        try:
            self.database = pyasn.pyasn(self.parameters.database)
        except IOError:
            self.logger.error("pyasn data file does not exist or could not be accessed in '%s'" % self.parameters.database)
            self.logger.error("Read 'bots/experts/asnlookup/README' and follow the procedure")
            self.stop()
    
    def process(self):
        error=False
	event = self.receive_message()
            
                    
        
        ip = event.value("ip_address")
               
        try:    
         info = self.database.lookup(ip)
        
         if info:
          if info[0]:
           event.update("asn", unicode(info[0]))
         
        except:
	 self.logger.info("There was an error parsing the event")
	 self.logger.info(event)
	 error=True	
        
	if not error:    
         self.send_message(event)
         self.acknowledge_message()
	else:
	 self.acknowledge_message()

if __name__ == "__main__":
    bot = fccnblacklist_ASNLookupExpertBot(sys.argv[1])
    bot.start()
