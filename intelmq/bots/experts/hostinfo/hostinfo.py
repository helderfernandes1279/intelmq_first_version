from intelmq.lib.bot import Bot, sys
from intelmq.lib.cache import Cache
from intelmq.lib.message import Event
import psycopg2


class hostinfoBot(Bot):
    
    def init(self):
        self.con = psycopg2.connect(
                                    database=self.parameters.database,
                                    user=self.parameters.user,
                                    password=self.parameters.password,
                                    host=self.parameters.host,
                                    port=self.parameters.port
                                   )
	self.cur = self.con.cursor()
        self.logger.info("Connected to PostgreSQL")

    def process(self):
        message = self.receive_message()

        if message:
            
            
            if isinstance(message, Event):
	       	                     
	       resultsrc=resultdst=None

	       if message.contains("source_ip"):
		  source_ip=message.value('source_ip')    
		  query = "select * from notes where '"+source_ip+"' <<= network(notes.cidr)"
	          self.cur.execute(query)
		  resultsrc=self.cur.fetchall()

               if message.contains("destination_ip"):  
                  destination_ip=message.value('destination_ip')
                  query = "select * from notes where '"+destination_ip+"' <<= network(notes.cidr)"
	          self.cur.execute(query)
		  resultdst=self.cur.fetchall()
                  
               if resultsrc:
		  for row in resultsrc:
                      if not message.contains('comment'):
                         message.add("comment","["+row[2]+"]")
		         self.logger.info("Info added")
                      else:
                         message.add("comment",message.value('comment')+'['+row[2]+']')
                         self.logger.info("Info added")
               if resultdst:
		  for row in resultdst: 	
		      if not message.contains('comment'):
                         message.add("comment","["+row[2]+"]")
                         self.logger.info("Info added")
                      else:
                         message.add("comment",message.value('comment')+'['+row[2]+']')
                         self.logger.info("Info added")
		     
		                         
            
	    self.send_message(message)
   

      
		

        self.acknowledge_message()


if __name__ == "__main__":
    bot = hostinfoBot(sys.argv[1])
    bot.start()
