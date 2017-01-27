import csv
import StringIO
from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Event
from intelmq.bots import utils
import ast

class splunk_alertsparser(Bot):

    def process(self):
        report = self.receive_message()
	report = ast.literal_eval(report)

        if report:
            rows = csv.DictReader(StringIO.StringIO(report['report']))
            
            for row in rows:
		event = Event()
		event.add('type',report['type'])
                for key, value in row.items():               
                  if key=='src_ip':
                     event.add('ip_address',value)
                event = utils.generate_observation_time(event, "last_seen")
                self.send_message(event)
        self.acknowledge_message()
   

if __name__ == "__main__":
    bot = splunk_alertsparser(sys.argv[1])
    bot.start()
