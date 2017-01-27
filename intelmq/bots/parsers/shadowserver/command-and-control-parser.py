import csv
import StringIO
from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Event
from intelmq.bots import utils

class ShadowServerCommandandControlParserBot(Bot):

    def process(self):
        report = self.receive_message()

        if report:
            report = report.strip()

            columns = {
                "ip": "source_ip",
                "port":"source_port",
		"channel": "additional_information",
                "asn": "source_asn",
		"as_name": "__IGNORE__",
		"as_desc": "__IGNORE__",
		"geo": "source_cc",
		"region": "__IGNORE__",
		"city": "__IGNORE__",
                "domain": "source_domain_name",
                "first_seen": "source_time"
            }
            
            rows = csv.DictReader(StringIO.StringIO(report))
            
            for row in rows:
                event = Event()
                
                for key, value in row.items():

                    key = columns[key]

                    if not value:
                        continue

                    value = value.strip()
                    
                    if key is "__IGNORE__" or key is "__TDB__":
                        continue
                    
                    if key is "additional_information":
			value = "Channel: " + value
		    # set timezone explicitly to UTC as it is absent in the input
                    if key == "source_time":
                        value += " UTC"
		
                    
                    event.add(key, value)
            
                event.add('feed', 'shadowserver-command-and-control')
                event.add('type', 'c&c')
		event.add('description','C&C Server')
                

                event = utils.parse_source_time(event, "source_time")  
                event = utils.generate_observation_time(event, "observation_time")
                event = utils.generate_reported_fields(event)
                
                self.send_message(event)
        self.acknowledge_message()
   

if __name__ == "__main__":
    bot = ShadowServerCommandandControlParserBot(sys.argv[1])
    bot.start()
