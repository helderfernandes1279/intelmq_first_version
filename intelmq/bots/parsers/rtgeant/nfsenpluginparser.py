from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Event
from intelmq.bots import utils
from datetime import datetime,timedelta
import pytz
import ast

class nfsenpluginParserBot(Bot):

    def process(self):
        tz=pytz.timezone('Europe/Lisbon')
        reports = self.receive_message()
	alertname=None
		
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
		      if pre_parsed_lines[count].startswith('Alert Name:'):
			 alertname=pre_parsed_lines[count].split(':')[1] 	
	    	      if pre_parsed_lines[count].startswith('#Evidence'):
	       		 startpos=count+1
            	      if pre_parsed_lines[count].startswith('Summary') and startpos!=0 and endpos==0:
	       		 endpos=count
	    	      count+=1

		
		#transformar o report em dicionario depois de garantir que existem linhas de report
		if startpos+1!=endpos:
		 eventlist=[]
		 columns=pre_parsed_lines[startpos].split(',')
		 for p in pre_parsed_lines[startpos+1:endpos]:
	   	     line=p.split(",")
		     parsed_line_report=dict()
	             for key, value in zip(columns, line):     
    	      	         parsed_line_report[key]=value	  
		     eventlist.append(parsed_line_report)	 
                 
		 
		 for eventline in eventlist:
                     event = Event()
		     event.add('rtir_id',report['id'])
		     event.add('description',report['subject'])
                     event.add('source_ip',eventline['sa'])
		     event.add('source_port',eventline['sp'])
                     event.add('destination_ip',eventline['da'])
		     event.add('destination_port',eventline['dp'])
		     event.add('transport_protocol',eventline['pr'].lower())
		     date_value=(tz.localize(datetime.strptime(eventline['ts'],'%Y-%m-%d %H:%M:%S'),is_dst=None).astimezone(pytz.utc)).strftime('%Y-%m-%d %H:%M:%S') + " UTC"
		     event.add('source_time',date_value)
                     event.add('feed', 'RT-FCCN_Nfsen')
                     event.add('feed_code', 'FCCN_Nfsen')
		     event.add('type', 'botnet drone')
		     event.add("additional_information","Possible C&C connection attempt occurred")
                     event = utils.generate_observation_time(event, "observation_time")
                     event = utils.generate_reported_fields(event)
                     self.send_message(event)
		     self.logger.info("Message sent")
                     
            self.acknowledge_message()


if __name__ == "__main__":
    bot = nfsenpluginParserBot(sys.argv[1])
    bot.start()

