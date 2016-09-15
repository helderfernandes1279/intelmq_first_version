from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Event
from intelmq.bots import utils
from datetime import datetime,timedelta
import pytz
import ast

class GEANTBLACKLISTParserBot(Bot):

    def process(self):
	tz=pytz.timezone('Europe/Lisbon')
        reports = self.receive_message()
	alerttype=None
	columns=['Source IP','Source port','Destination IP','Destination port','Protocol','Timestamp','Duration','Transferred','Packets','Flags','Source AS',
'Destination AS']
	
	
	reports=ast.literal_eval(reports)
        
        if reports:
            for report in reports:
		pre_parsed_lines=[]
		
		
		for p in report['message'].split('\n'):
	            pre_parsed_lines.append(p.strip())
		
                parsed_line_report=dict()
		count=0 
		startpos=0
	        endpos=0
		
		#Verificar qual e o inicio e o fim do array que contem a informacao do report 
       		while count<len(pre_parsed_lines):
	    	      if pre_parsed_lines[count].startswith('#Evidence'):
	       		 startpos=count+1
            	      if pre_parsed_lines[count]=='' and startpos!=0 and endpos==0:
	       		 endpos=count
	    	      count+=1
	
		#transformar o report em dicionario depois de garantir que existem linhas de report
		if startpos+1!=endpos:
		 eventlist=[]
		 for p in pre_parsed_lines[startpos+1:endpos]:
	   	     line=p.split(";")
		     parsed_line_report=dict()
	             for key, value in zip(columns, line):     
    	      	         parsed_line_report[key]=value	  
		     eventlist.append(parsed_line_report)	 
                 
		 
		 for eventline in eventlist:
                     event = Event()
		     event.add('rtir_id',report['id'])
		     event.add('description',report['subject'])
                     event.add('source_ip',eventline['Source IP'])
		     event.add('source_port',eventline['Source port'])
                     event.add('destination_ip',eventline['Destination IP'])
		     event.add('destination_port',eventline['Destination port'])
		     event.add('transport_protocol',eventline['Protocol'].lower())
		     date_value=(tz.localize(datetime.strptime(eventline['Timestamp'],'%Y-%m-%d %H:%M:%S.%f'),is_dst=None).astimezone(pytz.utc)).strftime('%Y-%m-%d %H:%M:%S') + " UTC"
		     event.add('source_time',date_value)
                     event.add('feed', 'RT-GEANT')
                     event.add('feed_code', 'GEANT')
		     event.add('type', 'botnet drone')
		     event.add("additional_information","Possible C&C connection attempt occurred")
                     event = utils.generate_observation_time(event, "observation_time")
                     event = utils.generate_reported_fields(event)
                     self.send_message(event)
		     self.logger.info("Message sent")
            self.acknowledge_message()


if __name__ == "__main__":
    bot = GEANTBLACKLISTParserBot(sys.argv[1])
    bot.start()

