import re
import imbox
import zipfile
from intelmq.lib.bot import Bot, sys
from intelmq.bots.collectors.mail.lib import Mail

class Splunk_MailAttachCollectorBot(Bot):

    def process(self):
        mailbox = imbox.Imbox(self.parameters.mail_host, self.parameters.mail_user, self.parameters.mail_password, self.parameters.mail_ssl)
        emails = mailbox.messages(folder=self.parameters.folder, unread=True)
	alert={}
        if emails:
            for uid, message in emails:
		
		subject=(message.subject).replace('\r\n','')
                if self.parameters.subject_regex and not re.search(self.parameters.subject_regex,subject):
		   continue
		self.logger.info(subject)
                self.logger.info("Reading email report")

		if subject[subject.find(':')+2:]=='Alertas Trojan Mirai Telnet Login Attempt':
		   alert['type']='Malware'
		if subject[subject.find(':')+2:]=='Alertas Intrusion Attempts':
		   alert['type']='Exploit'	
		if subject[subject.find(':')+2:]=='Alertas de Brute Force':
		   alert['type']='Brute Force'

                if hasattr(message,'attachments'):
		 for attach in message.attachments:
                    if not attach:
                        continue
                    
                    attach_name = attach['filename'][1:len(attach['filename'])-1] # remove quote marks from filename
                    
                    if re.search(self.parameters.attach_regex, attach_name):

                        if self.parameters.attach_unzip:
                            zipped = zipfile.ZipFile(attach['content'])
                            report = zipped.read(zipped.namelist()[0])
			    alert['report']=report
                        else:
                            report = attach['content'].read()
			    alert['report']=report
                            
                        self.send_message(alert)
                        
                mailbox.mark_seen(uid)
                self.logger.info("Email report read")


if __name__ == "__main__":
    bot = Splunk_MailAttachCollectorBot(sys.argv[1])
    bot.start()
