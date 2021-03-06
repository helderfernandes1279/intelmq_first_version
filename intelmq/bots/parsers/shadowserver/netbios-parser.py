import csv
import StringIO
from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Event
from intelmq.bots import utils

class ShadowServerNetbiosParserBot(Bot):

    def process(self):
        report = self.receive_message()

        if report:
            report = report.strip()

            columns = {
                "timestamp": "source_time",
                "ip": "source_ip",
		"protocol" : "transport_protocol",		
		"port" : "source_port",
		"hostname": "source_reverse_dns",
		"tag": "__IGNORE__",
		"mac_address": "__IGNORE__",
		"asn": "source_asn",
		"geo": "source_cc",
		"region" : "source_region",
		"city" : "source_city",
		"workgroup": "__IGNORE__",
		"machine_name": "source_local_hostname",
		"username":"__IGNORE__",
		"naics" : "__IGNORE__",
                "sic": "__IGNORE__"
            }           

            rows = csv.DictReader(StringIO.StringIO(report))

            for row in rows:
                event = Event()

                for key, value in row.items():
		    
                    if key=='sector':
			continue

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
            
                event.add('feed', 'shadowserver-netbios')
                event.add('type', 'vulnerable service')
                event.add('application_protocol', 'netbios')
		event.add('description','Netbios service detected')

                event = utils.parse_source_time(event, "source_time")  
                event = utils.generate_observation_time(event, "observation_time")
                event = utils.generate_reported_fields(event)
		
                self.send_message(event)
        self.acknowledge_message()
   

if __name__ == "__main__":
    bot = ShadowServerNetbiosParserBot(sys.argv[1])
    bot.start()
