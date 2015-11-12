import csv
import StringIO
from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Event
from intelmq.bots import utils

class ShadowServerCompromisedWebsitesParserBot(Bot):

    def process(self):
        report = self.receive_message()

        if report:
            report = report.strip()

            columns = {
                "timestamp": "source_time",
                "ip": "source_ip",
                "port": "source_port",
		"hostname": "source_reverse_dns",
		"tag": "malware",		
		"application": "application_protocol",
		"asn": "source_asn",
                "geo": "source_cc",
                "region": "source_region",
                "city": "source_city",
                "url": "source_url_secondpart",
		"http_host": "source_urlfirstpart",
		"category": "description",
		"system": "os_name",
		"detected_since": "__IGNORE__",
		"server": "__IGNORE__",
		"redirect_target": "__IGNORE__",
		"naics": "__IGNORE__",
		"sic": "__IGNORE__"
				
            }
            
            rows = csv.DictReader(StringIO.StringIO(report))
            
            for row in rows:
		event = Event()
		urlfirstpart=""
	        urlsecondpart=""
                port=""
		fullurl=""
                
		for key, value in row.items():

		    if key=='sector':
			continue

                    key = columns[key]

                    if not value:
                        continue

                    value = value.strip()
                    
                    if key is "__IGNORE__" or key is "__TBD__":
                       continue
                    
                    if key is "source_url_secondpart":
		       urlsecondpart=value
		       continue

		    if key is "source_urlfirstpart":
		       urlfirstpart=value
		       continue
		    
		    if key is "source_port":
		       port=value

		    if key is "malware":
                        value = value.strip().lower()
                        
                    # set timezone explicitly to UTC as it is absent in the input
                    if key == "source_time":
                        value += " UTC"
                    
                    event.add(key, value)
            	
		if port=="80":
		   fullurl="http://"
 		if port=="443":
		   fullurl="https://"
		
		fullurl=fullurl+urlfirstpart+"/"+urlsecondpart
                event.add('feed', 'shadowserver-websites')
                event.add('type', 'compromised')
                event.add('source_url', fullurl)
                event = utils.parse_source_time(event, "source_time")  
                event = utils.generate_observation_time(event, "observation_time")
                event = utils.generate_reported_fields(event)
                
                self.send_message(event)
        self.acknowledge_message()
   

if __name__ == "__main__":
    bot = ShadowServerCompromisedWebsitesParserBot(sys.argv[1])
    bot.start()
