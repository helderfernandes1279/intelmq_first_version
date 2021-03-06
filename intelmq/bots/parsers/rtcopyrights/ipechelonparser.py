from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Event
from intelmq.bots import utils
from datetime import datetime
import ast

class ipechelonParserBot(Bot):

    def process(self):

        reports = self.receive_message()
	

	
	
	reports=ast.literal_eval(reports)
        
        if reports:
	    badparsing=0
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
	    	      if pre_parsed_lines[count].startswith('Evidentiary Information'):
	       		 startpos=count+1
            	      if pre_parsed_lines[count]=='' and startpos!=0 and endpos==0:	
	       		 endpos=count
	    	      count+=1

				

		#transformar o report em dicionario depois de garantir que existem linhas de report
		if startpos!=endpos:
		 for p in pre_parsed_lines[startpos:endpos]:
	   	     line=p.split(": ")
		     if len(line)>1:
		        parsed_line_report[line[0]]=line[1]
		     else:
			self.logger.info("Bad Parsing")
			badparsing=1
		  
		
		 if badparsing==0:
                  event = Event()
		  event.add('rtir_id',report['id'])
		  event.add('description',report['subject'])
                  event.add('source_ip',parsed_line_report['Infringer\'s IP Address'])
		  event.add('source_port',parsed_line_report['Infringer\'s Port'])
		  event.add('application_protocol',parsed_line_report['Protocol'].lower())
		  event.add('additional_information','Content name:'+parsed_line_report['Infringed Work'] + ' | File name:'+parsed_line_report['Infringing FileName'] + ' | File size:'+parsed_line_report['Infringing FileSize'])
		  date_value=datetime.strptime(parsed_line_report['Initial Infringement Timestamp'][:-1],'%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S') + " UTC"
		  event.add('source_time',date_value)
                  event.add('feed', 'RT-ipechelon')
                  event.add('feed_code', 'ipechelon')
	 	  event.add('type', 'copyright')
                  event = utils.parse_source_time(event, "source_time")
                  event = utils.generate_observation_time(event, "observation_time")
                  event = utils.generate_reported_fields(event)
                  self.send_message(event)

        self.acknowledge_message()


if __name__ == "__main__":
    bot = ipechelonParserBot(sys.argv[1])
    bot.start()

