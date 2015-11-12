import csv
import StringIO
from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Event
from intelmq.bots import utils

class ShadowServerOpenResolverParserBot(Bot):

    def process(self):
        report = self.receive_message()

        if report:
            report = report.strip()

            columns = {
                "timestamp": "source_time",
                "ip": "source_ip",
		"asn": "source_asn",
		"geo": "source_cc",
		"region" : "source_region",
		"city" : "source_city",
		"port" : "source_port",
                "protocol" : "transport_protocol",
                "hostname": "source_reverse_dns",
		"min_amplification": "__IGNORE__",
                "dns_version" : "__IGNORE__",
                "p0f_genre" : "__IGNORE__",
                "p0f_detail": "__IGNORE__"
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
            
                event.add('feed', 'shadowserver-openresolver')
                event.add('type', 'vulnerable service')
                event.add('application_protocol', 'dns')
		event.add('description','DNS Open Resolver')

                event = utils.parse_source_time(event, "source_time")  
                event = utils.generate_observation_time(event, "observation_time")
                event = utils.generate_reported_fields(event)
		
                self.send_message(event)
        self.acknowledge_message()
   

if __name__ == "__main__":
    bot = ShadowServerOpenResolverParserBot(sys.argv[1])
    bot.start()