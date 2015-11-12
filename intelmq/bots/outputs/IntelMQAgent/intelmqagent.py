import time
import socket
from intelmq.lib.bot import Bot, sys

class IntelMQAgentBot(Bot):

    def process(self):  
	    
        event = self.receive_message()
        
        if event:
	   if self.parameters.feed!='':
	       if event.value('feed'):
                  event.clear('feed')
	       event.add('feed',self.parameters.feed)
	   if self.parameters.feed_url!='':
	       if event.value('feed_url'):
		  event.clear('feed_url')
	       event.add('feed_url',self.parameters.feed_url) 
 
           self.send_data(event.to_unicode())
          
            
        self.acknowledge_message()


    def connect(self):
        address = (self.parameters.ip, int(self.parameters.port))
        self.con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.con.connect(address)
        except socket.error, e:
            self.logger.error(e.args[1] + ". Retrying in 10 seconds.")
            time.sleep(10)

        self.logger.info("Connected successfully to %s:%i", address[0], address[1])

        
    def send_data(self, data):
            try:
		self.connect()
                self.con.sendall(data)
		self.logger.info("Data sent sucessfully")
		self.con.close()
            except socket.error, e:
                self.logger.error(e.args[1] + ". Reconnecting..")
                self.con.close()
                self.connect()


if __name__ == "__main__":
    bot = IntelMQAgentBot(sys.argv[1])
    bot.start()
