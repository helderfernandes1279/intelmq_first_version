import csv
import StringIO
from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Event
from intelmq.bots import utils

class ShadowServerisakmpParserBot(Bot):

    def process(self):
        report = self.receive_message()

        if report:
            report = report.strip()

            columns = {
                "timestamp": "source_time",
                "ip": "source_ip",
		"protocol":"transport_protocol",
		"port":"source_port",
		"hostname":"source_reverse_dns",
		"tag":"__IGNORE__",
                "asn": "source_asn",
		"geo": "source_cc",
		"region":"source_region",
		"city":"source_city",
		"naics":"__IGNORE__",
		"sic":"__IGNORE__",
		"initiator_spi":"__IGNORE__",
		"responder_spi":"__IGNORE__",
		"next_payload":"__IGNORE__",
		"exchange_type":"__IGNORE__",
		"flags":"__IGNORE__",
		"message_id":"__IGNORE__",
		"next_payload2":"__IGNORE__",
		"domain_of_interpretation":"__IGNORE__",
		"protocol_id":"__IGNORE__",
		"spi_size":"__IGNORE__",
		"notify_message_type":"__IGNORE__"
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
                    
		    
                    # set timezone explicitly to UTC as it is absent in the input
                    if key == "source_time":
                        value += " UTC"
		
                    
                    event.add(key, value)
            
                event.add('feed', 'shadowserver-isakmp')
                event.add('type', 'vulnerable service')
		event.add('description','ISAKMP vulnerable service')
                

                event = utils.parse_source_time(event, "source_time")  
                event = utils.generate_observation_time(event, "observation_time")
                event = utils.generate_reported_fields(event)
                
                self.send_message(event)
        self.acknowledge_message()
   

if __name__ == "__main__":
    bot = ShadowServerisakmpParserBot(sys.argv[1])
    bot.start()
