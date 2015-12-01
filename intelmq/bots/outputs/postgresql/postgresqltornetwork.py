import psycopg2,json,re,ipaddress
from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Event
import ast

class PostgreSQLBot_tor(Bot):

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
        record_list = self.receive_message()
        query   = "delete from tor_network" 
        self.cur.execute(query)
        record_list=ast.literal_eval(record_list)
        
        for record in record_list:	
            eventdict  = Event.from_unicode(record).to_dict()
            keys    = ", ".join(eventdict.keys())
            values  = eventdict.values()
            fvalues = len(values) * "%s, "
	    query  = "INSERT INTO tor_network (" + keys + ") VALUES (" + fvalues[:-2] + ")" 
	    self.logger.info(values)   
            self.cur.execute(query, values)
            self.con.commit()

        self.acknowledge_message()


if __name__ == "__main__":
    bot = PostgreSQLBot_tor(sys.argv[1])
    bot.start()
