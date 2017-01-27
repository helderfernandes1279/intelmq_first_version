import psycopg2
from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Event
import ast

class FCCN_blacklist_domains_PostgreSQLBot(Bot):

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
        domainslist = self.receive_message()
	domainslist=ast.literal_eval(domainslist)
        if domainslist:
	   feed=domainslist[0]['feed']
	   
	   query="DELETE from domain_blacklist where feed like '"+feed+"'"
	   
	   self.cur.execute(query)
	
	   for domain_record in domainslist:
	       domain=Event(domain_record)
	       evdict  = domain.to_dict()
               keys    = ", ".join(evdict.keys())
	       values  = evdict.values()
               fvalues = len(values) * "%s, "
               query   = "INSERT INTO domain_blacklist (" + keys + ") VALUES (" + fvalues[:-2] + ")"
               self.cur.execute(query, values)
	       
            
           self.con.commit()

        self.acknowledge_message()


if __name__ == "__main__":
    bot = FCCN_blacklist_domains_PostgreSQLBot(sys.argv[1])
    bot.start()
