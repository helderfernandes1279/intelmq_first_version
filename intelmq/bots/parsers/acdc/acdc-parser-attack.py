import json
from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Event
from intelmq.lib.utils import encode
from intelmq.bots import utils

class ACDCParserBot_attack(Bot):

    def process(self):
        report = self.receive_message()
	parsed_event=Event()
	
        
        if report:
	   if report.to_dict()['report']['report_category']=='eu.acdc.attack':
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

		 if report.to_dict()['report'].has_key('dst_ip_v4'):
		    parsed_event.add('destination_ip',report.to_dict()['report']['dst_ip_v4'])
		   
		 if report.to_dict()['report'].has_key('dst_port'):
		    parsed_event.add('destination_port',str(report.to_dict()['report']['dst_port']))

                 if report.to_dict()['report'].has_key('src_port'):
		    parsed_event.add('source_port',str(report.to_dict()['report']['src_port']))

		 parsed_event.add('source_domain_name',report.to_dict()['meta_data']['domain'])
		 parsed_event.add('source_time',report.to_dict()['report']['timestamp'])
		 

		 if report.to_dict()['report']['report_subcategory']=="dos":
		    parsed_event.add('type','dos')

		 elif report.to_dict()['report']['report_subcategory']=="abuse":
		      if report.to_dict()['report']['additional_data']['exploit']=="Portscan":
	                 parsed_event.add('type','scanner')
		      else: 
		         parsed_event.add('type','unknown')
		 elif report.to_dict()['report']['report_subcategory']=="login":
		      parsed_event.add('type','brute-force')
		 elif report.to_dict()['report']['report_subcategory']=="other":
		      parsed_event.add('type','ddos')
		 elif report.to_dict()['report']['report_subcategory']=="dos.tcp":
		      parsed_event.add('type','ddos')
		 else:
		      parsed_event.add('type','unknown')
		 
 		 parsed_event = utils.parse_source_time(parsed_event, "source_time")
        	 parsed_event = utils.generate_observation_time(parsed_event, "observation_time")
        	 parsed_event = utils.generate_reported_fields(parsed_event)
		 self.send_message(parsed_event)
   
        self.acknowledge_message()






if __name__ == "__main__":
    bot = ACDCParserBot_attack(sys.argv[1])
    bot.start()
