from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Event
from intelmq.bots import utils

class feodoParserBot(Bot):

    def process(self):
        report = self.receive_message()
	if report:
	   record_list=[]
	   report=report.split('\n')
           for line in report:
	       if line!='' and not line.startswith('#'):
		  record={}
	          record['ip']=line
		  record['subject']='feodo'
		  record_list.append(record)
	   self.send_message(record_list)		

	   
        
	self.acknowledge_message()
   

if __name__ == "__main__":
    bot = feodoParserBot(sys.argv[1])
    bot.start()

