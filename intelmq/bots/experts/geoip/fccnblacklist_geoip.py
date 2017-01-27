import geoip2.database
from intelmq.lib.bot import Bot, sys

class fccnblacklist_GeoIPExpertBot(Bot):

    def init(self):
        try:
            self.database = geoip2.database.Reader(self.parameters.database)
        except IOError:
            self.logger.error("GeoIP Database does not exist or could not be accessed in '%s'" % self.parameters.database)
            self.logger.error("Read 'bots/experts/geoip/README' and follow the procedure")
            self.stop()
    
    def process(self):
        event = self.receive_message()
        if event:  
           ip = event.value("ip_address")
                                     
           try:
             info = self.database.city(ip)
             if info.country.iso_code:
               event.add("cc", unicode(info.country.iso_code))
                       
             if info.city.name:
               event.add("city", unicode(info.city.name))

           except geoip2.errors.AddressNotFoundError:
             pass
            
           self.send_message(event)
        self.acknowledge_message()

if __name__ == "__main__":
    bot = fccnblacklist_GeoIPExpertBot(sys.argv[1])
    bot.start()
