import psycopg2
from intelmq.lib.bot import Bot, sys

class FCCN_blacklist_PostgreSQLBot(Bot):

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
        if event:
	 if event.value ('entity')=='external':
	    event.clear('entity')
            evdict  = event.to_dict()
            keys    = ", ".join(evdict.keys())
	    
            ipaddress=event.value('ip_address')	
	    
	    #verificar se o IP está na blacklist
	    query="select ip_address from fccn_blacklist where ip_address='"+ipaddress+"'"

            self.cur.execute(query)
            result=self.cur.fetchone()  
	    
            if result:	            
	       query="UPDATE fccn_blacklist SET (last_seen) = ('"+event.value('last_seen')+"') WHERE ip_address='"+ipaddress+"'"
	       self.cur.execute(query)
	       self.logger.info("Last seen updated for %s" % ipaddress)
	    else:
	       values  = evdict.values()
               fvalues = len(values) * "%s, "
               query   = "INSERT INTO fccn_blacklist (" + keys + ") VALUES (" + fvalues[:-2] + ")"
               self.cur.execute(query, values)
	       self.logger.info("New IP inserted")
            
            self.con.commit()

        self.acknowledge_message()


if __name__ == "__main__":
    bot = FCCN_blacklist_PostgreSQLBot(sys.argv[1])
    bot.start()
