import csv
import StringIO
from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Event
from intelmq.bots import utils

class ShadowServerDroneParserBot(Bot):

    def process(self):
        report = self.receive_message()

        if report:
            report = report.strip()

            columns = {
                "timestamp": "source_time",
                "ip": "source_ip",
                "port": "source_port",
                "asn": "source_asn",
                "geo": "source_cc",
                "region": "source_region",
                "city": "source_city",
                "hostname": "source_reverse_dns",
                "type": "__IGNORE__",
                "infection": "malware",
                "url": "destination_url",
                "agent": "user_agent",
                "cc_ip": "destination_ip",
                "cc_port": "destination_port",
                "cc_asn": "destination_asn",
                "cc_geo": "destination_cc",
                "cc_dns": "destination_reverse_dns",
                "count": "__TBD__",
                "proxy": "__TBD__",
                "application": "__TBD__",
                "p0f_genre": "__TBD__",
                "p0f_detail": "__TBD__",
                "machine_name": "__TBD__",
                "id": "__TBD__",
		"naics": "__IGNORE__",
		"sic": "__IGNORE__",
		"cc_naics": "__IGNORE__",
		"cc_sic": "__IGNORE__",
		"sector": "__IGNORE__",
		"cc_sector":"__IGNORE__",
		"ssl_cipher": "__IGNORE__",
		"family": "__IGNORE__",
		"tag": "__IGNORE__",
		"public_source": "__IGNORE__"			
            }
           

            rows = csv.DictReader(StringIO.StringIO(report))
            
            for row in rows:
		event = Event()
		fullurl = ""
		port = None
                for key, value in row.items():
		
                    key = columns[key]

                    if not value:
                        continue

                    value = value.strip()
                    
                    if key is "__IGNORE__" or key is "__TBD__":
                        continue
                    
                    if key is "malware":
                        value = value.strip().lower()
                     
		    if key is "destination_port":
		        port=value
   
                    # set timezone explicitly to UTC as it is absent in the input
                    if key == "source_time":
                        value += " UTC"
                    
                    event.add(key, value)

            	if port=="80":
		   fullurl="http://"
 		if port=="443":
		   fullurl="https://"
		
		if event.value('destination_reverse_dns') != None and event.value('destination_url')!= None:
                   fullurl=fullurl+event.value('destination_reverse_dns')+event.value('destination_url')
		   event.clear('destination_url')
		   event.add('destination_url',fullurl)
                
		event.add('feed', 'shadowserver-drone')
                event.add('type', 'botnet drone')
                event = utils.parse_source_time(event, "source_time")  
                event = utils.generate_observation_time(event, "observation_time")
                event = utils.generate_reported_fields(event)
                
                self.send_message(event)
        self.acknowledge_message()
   

if __name__ == "__main__":
    bot = ShadowServerDroneParserBot(sys.argv[1])
    bot.start()
