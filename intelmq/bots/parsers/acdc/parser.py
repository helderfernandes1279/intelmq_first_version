import json
from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Event
from intelmq.lib.utils import encode
from intelmq.bots import utils

class ACDCParserBot(Bot):

    def process(self):
        report = self.receive_message()
	
        
        if report:
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
          self.send_message(report)
         except ValueError:
          self.logger.info("Event not parsed correctly")
          self.send_message(report)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = ACDCParserBot(sys.argv[1])
    bot.start()
