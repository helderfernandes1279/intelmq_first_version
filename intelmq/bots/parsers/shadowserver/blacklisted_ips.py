import csv
import StringIO
from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Event
from intelmq.bots import utils

class blacklist_ips_ParserBot(Bot):

    def process(self):
        report = self.receive_message()

        if report:
            report = report.strip()

            columns = {
		"timestamp": "source_time",
                "ip": "source_ip",
		"hostname":"source_reverse_dns",
		"source":"source",
		"reason":"reason",
                "asn": "source_asn",
		"geo": "source_cc",
		"region": "__IGNORE__",
		"city": "__IGNORE__",
                "naics": "__IGNORE__",
		"sic":"__IGNORE__",
                "sector": "__IGNORE__"
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
                    
		    if key is "source":
			concat_value='Source->'+value
			continue
		    if key is "reason":
			concat_value=concat_value+'  '+'reason->'+value
		    	continue

                    # set timezone explicitly to UTC as it is absent in the input
                    if key == "source_time":
                        value += " UTC"
		
                    
                    event.add(key, value)
            
                event.add('feed', 'shadowserver-blacklist')
                event.add('type', 'blacklist')
		event.add('description',concat_value)
                

                event = utils.parse_source_time(event, "source_time")  
                event = utils.generate_observation_time(event, "observation_time")
                event = utils.generate_reported_fields(event)
                
                self.send_message(event)
        self.acknowledge_message()
   

if __name__ == "__main__":
    bot = blacklist_ips_ParserBot(sys.argv[1])
    bot.start()
