from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Event
from intelmq.bots import utils

class ZeusParserBot(Bot):

    def process(self):
        report = self.receive_message()
	if report:
	   iplist=[]
	   report=report.split('\n')
           for line in report:
	       if line!='' and not line.startswith('#'):
	          iplist.append(line)

	   self.send_message(iplist)
        
	self.acknowledge_message()
   

if __name__ == "__main__":
    bot = ZeusParserBot(sys.argv[1])
    bot.start()

