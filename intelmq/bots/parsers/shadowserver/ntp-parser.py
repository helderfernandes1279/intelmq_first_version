import csv
import StringIO
from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Event
from intelmq.bots import utils

class ShadowServerNTPParserBot(Bot):

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
		"asn": "source_asn",
		"geo": "source_cc",
		"region" : "source_region",
                "city" : "source_city",
		"version": "__IGNORE__",
		"clk_wander": "__IGNORE__",
		"clock": "__IGNORE__",
		"error": "__IGNORE__",
		"frequency": "__IGNORE__",
		"jitter": "__IGNORE__",
		"leap": "__IGNORE__",
		"mintc": "__IGNORE__",
		"noise": "__IGNORE__",
		"offset": "__IGNORE__",
		"peer": "__IGNORE__",
		"phase": "__IGNORE__",
		"poll": "__IGNORE__",
		"precision": "__IGNORE__",
		"processor": "__IGNORE__",
		"refid": "__IGNORE__",
		"reftime": "__IGNORE__",
		"rootdelay": "__IGNORE__",
		"rootdispersion": "__IGNORE__",
		"stability": "__IGNORE__",
		"state": "__IGNORE__",
		"stratum": "__IGNORE__",
		"system": "__IGNORE__",
		"tai": "__IGNORE__",
		"tc": "__IGNORE__",    
		"naics" : "__IGNORE__",
		"sic": "__IGNORE__",
		"sector":"__IGNORE__"
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
            
                event.add('feed', 'shadowserver-ntp')
                event.add('type', 'vulnerable service')
                event.add('application_protocol', 'ntp')
		event.add('description','NTP Service')

                event = utils.parse_source_time(event, "source_time")  
                event = utils.generate_observation_time(event, "observation_time")
                event = utils.generate_reported_fields(event)
		
                self.send_message(event)
        self.acknowledge_message()
   

if __name__ == "__main__":
    bot = ShadowServerNTPParserBot(sys.argv[1])
    bot.start()
