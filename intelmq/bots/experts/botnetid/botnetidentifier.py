from intelmq.lib.bot import Bot, sys
from intelmq.lib.cache import Cache
from intelmq.lib.message import Event
import psycopg2


class botnetIDBot(Bot):
    
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
	       
	       source_ip=message.value('source_ip')
	       destination_ip=message.value('destination_ip')                 
	       
	       if message.contains("source_ip") and message.contains("destination_ip") and message.value('type')=='botnet drone': 
		  query = "select description from botnet_servers where ip='"+source_ip+"' or ip='"+destination_ip+"'"
	          self.cur.execute(query)
		  result=self.cur.fetchone()  

                  if result:
		     message.add("malware","%s-family" % result)
		               
            
	    self.send_message(message)
   

      
		

        self.acknowledge_message()


if __name__ == "__main__":
    bot = botnetIDBot(sys.argv[1])
    bot.start()
