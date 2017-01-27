from intelmq.lib.bot import Bot, sys
import smtplib 
from email.mime.multipart import MIMEMultipart
from email.Utils import COMMASPACE, formatdate
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email.header import Header
from email import Encoders

class FCCN_blacklist_IntelMQMailerBot(Bot):

    def process(self):
        event = self.receive_message()
        event_msg="\nEvent Details:\n\n"
	if event:
	 
	 if not event.value('entity')=='external':
            for key in event.keys():
		event_msg+=key+' : '+event.value(key)+'\n'
            self.sendmail(self.parameters.send_from,[self.parameters.send_to],self.parameters.subject,event_msg,self.parameters.smtpserver)    
        self.acknowledge_message()
	
   



    def sendmail(self,send_from, send_to, subject, text,server):
       	
	assert type(send_to)==list
    	msg = MIMEMultipart()
    	msg['From'] = send_from
    	msg['To'] = COMMASPACE.join(send_to)
    	msg['Date'] = formatdate(localtime=True)
    	msg['Subject'] = Header(subject,'utf-8')
    	msg.attach(MIMEText(text, 'plain', 'utf-8') )
    	smtp = smtplib.SMTP(server,25)
    	smtp.sendmail(send_from, send_to, msg.as_string())
    	smtp.close()
       
if __name__ == "__main__":
    bot = FCCN_blacklist_IntelMQMailerBot(sys.argv[1])
    bot.start()
