import csv
import StringIO 
from intelmq.lib.bot import Bot, sys
from datetime import datetime
from intelmq.lib.message import Event
from intelmq.lib.utils import encode

class TorParserBot(Bot):

    def process(self):
        report = self.receive_message()
	report = encode(report)

	if report:
            columns = {
                "Router Name": "routername",
                "Country Code": "countrycode",
                "Bandwidth (KB/s)": "__IGNORE__",
                "Uptime (Hours)": "uptime",
                "IP Address": "ipaddress",
                "Hostname": "hostname",
                "ORPort": "orport",
                "DirPort": "dirport",
                "Flag - Authority": "__IGNORE__",
                "Flag - Exit": "flagexit",
                "Flag - Fast": "__IGNORE__",
                "Flag - Guard": "__IGNORE__",
                "Flag - Named": "__IGNORE__",
                "Flag - Stable": "__IGNORE__",
                "Flag - Running": "flagrunning",
                "Flag - Valid":  "__IGNORE__",
                "Flag - V2Dir":  "__IGNORE__",
                "Platform":  "__IGNORE__",
                "Flag - Hibernating":  "__IGNORE__",
                "Flag - Bad Exit":  "__IGNORE__",
                "FirstSeen": "firstseen",
                "ASName": "asname",
                "ASNumber": "asnumber",
                "ConsensusBandwidth":  "__IGNORE__",
                "OrAddress": "__IGNORE__"
            }
            
            rows = csv.DictReader(StringIO.StringIO(report))
            record_list=[]
            for row in rows:
                event = Event()
                
                for key, value in row.items():

                    key = columns[key]
		    value = value.strip()


                    if (not value) or (value.lower()=='none') or (value.lower()=='n/a'):
                        continue
                    
                    
                    
                    if key is "__IGNORE__":
                        continue
                    
             
                    if key is "firstseen":
			self.logger.info(value)
			value=datetime.strptime(value,'%Y-%m-%d').strftime('%Y-%m-%d')                        
                        
                    event.add(key, value)
                record_list.append(unicode(event))    
            self.send_message(record_list)
            self.acknowledge_message()

if __name__ == "__main__":
    bot = TorParserBot(sys.argv[1])
    bot.start()

