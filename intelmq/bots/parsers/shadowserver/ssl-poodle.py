import csv
import StringIO
from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Event
from intelmq.bots import utils

class ShadowServerSSLpoodleParserBot(Bot):

    def process(self):
        report = self.receive_message()

        if report:
            report = report.strip()

            columns = {
                "timestamp": "source_time",
                "ip": "source_ip",
		"port" : "source_port",
		"hostname": "source_reverse_dns",
		"tag": "__IGNORE__",
		"handshake": "__IGNORE__",
		"asn": "source_asn",
		"geo": "source_cc",
		"region" : "source_region",
		"city" : "source_city",
		"cipher_suite": "__IGNORE__",
		"ssl_poodle": "__IGNORE__",
		"cert_length": "__IGNORE__",
		"subject_common_name": "__IGNORE__",
		"issuer_common_name": "__IGNORE__",
		"cert_issue_date": "__IGNORE__",
		"cert_expiration_date": "__IGNORE__",
		"sha1_fingerprint": "__IGNORE__",
		"cert_serial_number": "__IGNORE__",
		"ssl_version": "__IGNORE__",
		"signature_algorithm": "__IGNORE__",
		"key_algorithm": "__IGNORE__",
		"subject_organization_name": "__IGNORE__",
		"subject_organization_unit_name": "__IGNORE__",
		"subject_country": "__IGNORE__",
		"subject_state_or_province_name": "__IGNORE__",
		"subject_locality_name": "__IGNORE__",
		"subject_street_address": "__IGNORE__",
		"subject_postal_code": "__IGNORE__",
		"subject_surname": "__IGNORE__",
		"subject_given_name": "__IGNORE__",
		"subject_email_address": "__IGNORE__",
		"subject_business_category": "__IGNORE__",
		"subject_serial_number": "__IGNORE__",
		"issuer_organization_name": "__IGNORE__",
		"issuer_organization_unit_name": "__IGNORE__",
		"issuer_country": "__IGNORE__",
		"issuer_state_or_province_name": "__IGNORE__",
		"issuer_locality_name": "__IGNORE__",
		"issuer_street_address": "__IGNORE__",
		"issuer_postal_code": "__IGNORE__",
		"issuer_surname": "__IGNORE__",
		"issuer_given_name": "__IGNORE__",
		"issuer_email_address": "__IGNORE__",
		"issuer_business_category": "__IGNORE__",
		"issuer_serial_number": "__IGNORE__",
		"naics": "__IGNORE__",
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
            
                event.add('feed', 'shadowserver-sslpoodle')
                event.add('type', 'vulnerable service')
		event.add('description','SSL Poodle Vulnerability')

                event = utils.parse_source_time(event, "source_time")  
                event = utils.generate_observation_time(event, "observation_time")
                event = utils.generate_reported_fields(event)
		
                self.send_message(event)
        self.acknowledge_message()
   

if __name__ == "__main__":
    bot = ShadowServerSSLpoodleParserBot(sys.argv[1])
    bot.start()
