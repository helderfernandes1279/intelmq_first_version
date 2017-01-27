import csv
import StringIO
from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Event
from intelmq.bots import utils

class ShadowServeropenLdapParserBot(Bot):

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
		"size":"__IGNORE__",
		"configuration_naming_context":"additional_information",
		"current_time":"__IGNORE__",
		"default_naming_context":"__IGNORE__",
		"dns_host_name":"source_local_hostname",
		"domain_controller_functionality":"__IGNORE__",
		"domain_functionality":"__IGNORE__",
		"ds_service_name":"__IGNORE__",
		"forest_functionality":"__IGNORE__",
		"highest_committed_usn":"__IGNORE__",
		"is_global_catalog_ready":"__IGNORE__",
		"is_synchronized":"__IGNORE__",
		"ldap_service_name":"__IGNORE__",
		"naming_contexts":"__IGNORE__",
		"root_domain_naming_context":"__IGNORE__",
		"schema_naming_context":"__IGNORE__",
		"server_name":"__IGNORE__",
		"subschema_subentry":"__IGNORE__",
		"supported_capabilities":"__IGNORE__",
		"supported_control":"__IGNORE__",
		"supported_ldap_policies":"__IGNORE__",
		"supported_ldap_version":"__IGNORE__",
		"supported_sasl_mechanisms":"__IGNORE__"
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
		    if key== "additional_information":
			value ="configuration_naming_context->"+value
                    
                    event.add(key, value)
            
                event.add('feed', 'shadowserver-openldap')
                event.add('type', 'vulnerable service')
		event.add('description','Open LDAP Service detected')
                

                event = utils.parse_source_time(event, "source_time")  
                event = utils.generate_observation_time(event, "observation_time")
                event = utils.generate_reported_fields(event)
                
                self.send_message(event)
        self.acknowledge_message()
   

if __name__ == "__main__":
    bot = ShadowServeropenLdapParserBot(sys.argv[1])
    bot.start()
