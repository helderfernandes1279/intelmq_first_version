import psycopg2,ast
from intelmq.lib.bot import Bot, sys
import json

class PostgreSQLBotnetservers_fccn(Bot):

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
        iplist = self.receive_message()
	
        if iplist:
	   iplist=(iplist.strip('[]')).replace('}, {','}|{')
	   iplist=iplist.split('|')
	   record=ast.literal_eval(iplist[0])
           query   = "delete from botnet_servers where description like '" + record['subject'] + "'" 
	   self.cur.execute(query)
           	

	   for record in iplist:
	       record=ast.literal_eval(record)
               query   = "INSERT INTO botnet_servers (ip,description) VALUES (%s,%s)"
               try:
	          self.cur.execute(query,[record['ip'],record['subject']])
               except Exception,e:
                  self.logger.info(e)
	   self.con.commit()	
            

        self.acknowledge_message()

   
if __name__ == "__main__":
    bot = PostgreSQLBotnetservers_fccn(sys.argv[1])
    bot.start()
