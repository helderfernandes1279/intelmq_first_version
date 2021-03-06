import os.path
import time
import json
import redis
from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout
from intelmq.lib.bot import Bot, sys

class XMPPCollectorBot(Bot):
    
    xmpp=None
    
    def process(self):  
        
       if self.xmpp is None:	
	self.xmpp = ACDCXMPPBot(self.parameters.xmpp_user+'@'+self.parameters.xmpp_server, self.parameters.xmpp_key,self.send_message,self.logger)
        self.xmpp.connect(reattempt=True)
        self.xmpp.process()
       else:
	self.logger.info("Connection is Alive")
    def killbot(self):
	self.xmpp.disconnect(wait=True)
	self.logger.info("XMPP Disconnected") 	
	
	

class ACDCXMPPBot(ClientXMPP):
        
        def __init__(self,jid,password,objects,objectl):
                ClientXMPP.__init__(self,jid,password)
                self.add_event_handler("session_start", self.session_start)
                self.add_event_handler("message",self.message_logging)
		self.collectorl=objectl
		self.collectorl.info("XMPP connected")
		self.collectors=objects


        def session_start(self,event):
                self.send_presence()
                self.get_roster()

         
        def message_logging(self,msg):
                #log_file.write("Timestamp:%s From:%s Body:%s\n" % (time.strftime("%H:%M:%S"),msg['from'], msg['body']))
		event=msg['body']
		self.collectors(event)	

if __name__ == "__main__":
    bot = XMPPCollectorBot(sys.argv[1])
    bot.start()
