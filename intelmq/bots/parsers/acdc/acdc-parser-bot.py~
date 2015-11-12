import json
from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Event
from intelmq.lib.utils import encode
from intelmq.bots import utils

class ACDCParserBot_bot(Bot):

    def process(self):
        report = self.receive_message()
	parsed_event=Event()
	
        
        if report:
	   if report.to_dict()['report']['report_category']=='eu.acdc.bot':
	         if(report.to_dict()['report'].has_key('sample_b64')):	
		    report.to_dict()['report']['sample_b64']='ficheiro binario'
		    self.logger.info('field changed')	
	
		 tmp=(report.value('report')).get('report_type')
   		 try:
		  categ=tmp[tmp.index('[')+1:tmp.index('][')]
   		  sensor=tmp[tmp.index('][')+2:tmp.index('][',tmp.index('][')+2)]
   		  entity=tmp[tmp.index('][',tmp.index('][')+2)+2:tmp.index(']',tmp.index('][',tmp.index('][')+2)+2)]
   		  description=tmp.split(']')[3][1:]
		  value1=json.dumps({"Category":"%s"%categ,"Sensor":"%s"%sensor,"Entity":"%s"%entity,"Description":"%s"%description})
		  value=json.loads(value1)
		  report.add('Additional Info',value)
        	 except ValueError:
        	  self.logger.info("Event not parsed correctly")
          
         

		 if report.to_dict().has_key('Additional Info'):
		  parsed_event.add('feed','ACDC:'+report.to_dict()['Additional Info']['Entity'])
		  parsed_event.add('additional_information',report.to_dict()['Additional Info']['Description'])
        	 else:
		  parsed_event.add('feed','ACDC:'+report.to_dict()['report']['report_type'])

		 parsed_event.add('feed_code','ACDC:'+str(report.to_dict()['meta_data']['id']))
		 parsed_event.add('description',report.to_dict()['report']['report_category'])
		 parsed_event.add('source_ip',report.to_dict()['report']['src_ip_v4'])
		 parsed_event.add('source_port',str(report.to_dict()['report']['src_port']))
		 parsed_event.add('source_domain_name',report.to_dict()['meta_data']['domain'])
		 parsed_event.add('source_time',report.to_dict()['report']['timestamp'])
		 if report.to_dict()['report']['report_subcategory']=="fast_flux":
		    parsed_event.add('type','fastflux')
		 else:
		    parsed_event.add('type','malware')
		
		 if report.to_dict()['report'].has_key('c2_ip_v4'):
		    parsed_event.add('destination_ip',report.to_dict()['report']['c2_ip_v4'])
		    parsed_event.add('destination_port',str(report.to_dict()['report']['c2_port']))	
			

 		 parsed_event = utils.parse_source_time(parsed_event, "source_time")
        	 parsed_event = utils.generate_observation_time(parsed_event, "observation_time")
        	 parsed_event = utils.generate_reported_fields(parsed_event)
		 self.send_message(parsed_event)
   
        self.acknowledge_message()






if __name__ == "__main__":
    bot = ACDCParserBot_bot(sys.argv[1])
    bot.start()
