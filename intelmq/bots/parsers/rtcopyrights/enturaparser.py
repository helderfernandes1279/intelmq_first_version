from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Event
from intelmq.bots import utils
from datetime import datetime
import ast

class enturaParserBot(Bot):

    def process(self):

        reports = self.receive_message()
	

       	
	
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
	    	      if pre_parsed_lines[count].startswith('Below are the details relating to the observed infringement:'):
	       		 startpos=count+2
            	      if pre_parsed_lines[count].startswith('Filesize') and startpos!=0 and endpos==0:	
	       		 endpos=count+1
	    	      count+=1

				
	
		#transformar o report em dicionario depois de garantir que existem linhas de report
		if startpos!=endpos:
		 for p in pre_parsed_lines[startpos:endpos]:
	   	     line=p.split(": ")	
		     if len(line)>1:
                        parsed_line_report[line[0]]=line[1].strip()
	  	 
                 event = Event()
		 event.add('rtir_id',report['id'])
		 event.add('description',report['subject'])
                 event.add('source_ip',parsed_line_report['IP Address'])
		 event.add('source_port',parsed_line_report['Port'])
		 event.add('application_protocol',parsed_line_report['Type'].lower())
		 event.add('additional_information','Content name:'+parsed_line_report['Title'] + ' | File name:'+parsed_line_report['Filename'] + ' | File size:'+parsed_line_report['Filesize'])
		 date_value=datetime.strptime(parsed_line_report['Timestamp'][:-1],'%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S') + " UTC"
		 event.add('source_time',date_value)
                 event.add('feed', 'RT-Entura Ltd')
                 event.add('feed_code', 'Entura Ltd')
	 	 event.add('type', 'copyright')
                 event = utils.parse_source_time(event, "source_time")
                 event = utils.generate_observation_time(event, "observation_time")
                 event = utils.generate_reported_fields(event)
		 self.logger.info(event)                 
		 self.send_message(event)
	    self.acknowledge_message()


if __name__ == "__main__":
    bot = enturaParserBot(sys.argv[1])
    bot.start()

