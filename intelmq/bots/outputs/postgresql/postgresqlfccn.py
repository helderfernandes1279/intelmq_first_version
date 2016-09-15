import psycopg2,json,re,ipaddress
from intelmq.lib.bot import Bot, sys

class PostgreSQLBot_fccn(Bot):

    def init(self):
        self.logger.debug("Connecting to PostgreSQL")
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
        event = self.receive_message()
	constituency_element=False
        if event:
            evdict  = event.to_dict()
            keys    = ", ".join(evdict.keys())
            values  = evdict.values()
            fvalues = len(values) * "%s, "
		
	    src_entity=event.value('source_entity')
	    dst_entity=event.value('destination_entity')
	    
	    if src_entity:
	       if re.search("FCCN",src_entity): 
		  constituency_element=True
		   
      
            if dst_entity:
	       if re.search("FCCN",dst_entity):
		  constituency_element=True
		  


	    if constituency_element:	
	       query   = "INSERT INTO events_constituency (" + keys + ") VALUES (" + fvalues[:-2] + ")"
	    else:	
               query   = "INSERT INTO events (" + keys + ") VALUES (" + fvalues[:-2] + ")"
            
           
	    self.cur.execute(query, values)
            self.con.commit()
	    

        self.acknowledge_message()

   
if __name__ == "__main__":
    bot = PostgreSQLBot_fccn(sys.argv[1])
    bot.start()
