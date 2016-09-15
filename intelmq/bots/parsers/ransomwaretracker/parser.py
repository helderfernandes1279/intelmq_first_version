from copy import deepcopy
from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Event
from intelmq.bots import utils

class RansomWareParserBot(Bot):

    def process(self):
        report = self.receive_message()
	
	if report:
	   event = Event()
	   record_list=[]
	   report=report.split('\n')
           for line in report:
	       if line!='' and not line.startswith('#') and not line=='ERROR: Too many connections':
		  event = Event()
		  values=line.split(',')
		  self.logger.info(values)
		  event.add('source_time',values[0].strip('"')+" UTC")
		  event.add('additional_information',values[1].strip('"'))
		  event.add('malware',values[2].strip('"'))
		  event.add('source_domain_name',values[3].strip('"'))
		  event.add('source_url',values[4].strip('"'))
		  event.add('status',values[5].strip('"'))
		  event.add('feed','abuse.ch')
		  event.add('type','ransomware')
		  event = utils.parse_source_time(event, "source_time")  
                  event = utils.generate_observation_time(event, "observation_time")
                  iplist=[]
		  iplist=values[6].split('|')
		  for ip in iplist:
		      message=deepcopy(event)
		      message.add('source_ip',ip.strip('"'))
		      message=utils.generate_reported_fields(message)
		      self.send_message(message) 		

        
	self.acknowledge_message()
   

if __name__ == "__main__":
    bot = RansomWareParserBot(sys.argv[1])
    bot.start()
