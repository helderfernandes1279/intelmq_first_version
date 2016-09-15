from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Event
from intelmq.bots import utils
from datetime import datetime
import ast

class arborDoSParserBot(Bot):

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
		     	
	    	      if pre_parsed_lines[count].startswith('DoS host detection') and 'ended' not in pre_parsed_lines[count]:
			 alertdate=pre_parsed_lines[count][-24:].strip(' GMT.')
	       		 startpos=count+2
            	      if "Managed Objects" in pre_parsed_lines[count] and startpos!=0 and endpos==0:	
	       		 endpos=count
	    	      count+=1

				
                
		#transformar o report em dicionario depois de garantir que existem linhas de report
		if startpos!=endpos:
	         
		 for p in pre_parsed_lines[startpos:endpos]:
	   	     line=p.split(":  ")	
		     parsed_line_report[line[0]]=line[1]
				  
		
		
                 event = Event()
		 event.add('rtir_id',report['id'])
		 event.add('description',report['subject'])
                 event.add('destination_ip',parsed_line_report['Host'])
		 event.add('additional_information','Signatures:'+parsed_line_report['Signatures'] + ' | Impact:'+parsed_line_report['Impact'])
		 date_value=datetime.strptime(alertdate,'%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S') + " UTC"
		 event.add('source_time',date_value)
                 event.add('feed', 'Arbor Peakflow')
                 event.add('feed_code', 'Peakflow')
		 event.add('description_url',parsed_line_report['URL']) 
	 	 event.add('type', 'dos')
                 event = utils.parse_source_time(event, "source_time")
                 event = utils.generate_observation_time(event, "observation_time")
                 event = utils.generate_reported_fields(event)
		 self.logger.info("message sent")
                 self.send_message(event)

        self.acknowledge_message()


if __name__ == "__main__":
    bot = arborDoSParserBot(sys.argv[1])
    bot.start()

