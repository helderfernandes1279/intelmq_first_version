import json
from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Event
from intelmq.lib.utils import encode
from intelmq.bots import utils

class ACDCParserBot_maliciousuri(Bot):

    def process(self):
        report = self.receive_message()
	parsed_event=Event()
	
        
        if report:
	   if report.to_dict()['report']['report_category']=='eu.acdc.malicious_uri':
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
		 parsed_event.add('source_url',report.to_dict()['report']['source_value'])
		 parsed_event.add('source_time',report.to_dict()['report']['timestamp'])
                 parsed_event.add('source_domain_name',report.to_dict()['meta_data']['domain'])
		
		 
		 if report.to_dict()['report']['report_subcategory']=="other":
		    if report.to_dict().has_key('Additional Info'):
		       if report.to_dict()['Additional Info']['Description']=="- Defacement":
                          parsed_event.add('type','defacement')
		    else:
		       parsed_event.add('type','unknown')
		 else:
		    parsed_event.add('type',report.to_dict()['report']['report_subcategory'])

 		 parsed_event = utils.parse_source_time(parsed_event, "source_time")
        	 parsed_event = utils.generate_observation_time(parsed_event, "observation_time")
        	 parsed_event = utils.generate_reported_fields(parsed_event)
		 self.send_message(parsed_event)
   
        self.acknowledge_message()






if __name__ == "__main__":
    bot = ACDCParserBot_maliciousuri(sys.argv[1])
    bot.start()
