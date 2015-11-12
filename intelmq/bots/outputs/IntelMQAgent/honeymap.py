import time, socket,base64,json
from intelmq.lib.bot import Bot, sys,Event

class IntelMQAgentBot(Bot):

    def process(self):  
	    
        event = self.receive_message()
        
        if event:
	    data=Event()
	    
	    columns = {
                "latitude": "source_latitude",
                "longitude": "source_longitude",
                "latitude2" : "destination_latitude",
                "longitude2": "destination_longitude",
                "type": "type"
            }           
 	    
            for key in columns.keys():
		
		keytmp = columns[key]
		value=event.value(keytmp)
		if value:
		   if key=="latitude" or key=="longitude" or key=="latitude2" or key=="longitude2": 
                      data.add(key, float(value))
		   else:
		      data.add(key, value)
	   	
            if data.value("latitude") and data.value("longitude"):
	       self.send_data(data)
            
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
		data=str(unicode(data))
		
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
