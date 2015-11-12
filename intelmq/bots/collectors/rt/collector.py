from intelmq.lib.bot import Bot, sys
from intelmq.bots.collectors.url.lib import fetch_url
from rt_objects import *


class RTCollectorBot(Bot): 
    
       
    def process(self):
	rtuser = self.parameters.rtusername  
    	rtpassword = self.parameters.rtpassword 
    	rt_url = self.parameters.rt_url 
    	subject_filter=self.parameters.subject
	from_id=self.parameters.fromid 
    	rt_rest_url = rt_url + 'REST/1.0/'
	rt_display_ticket = rt_url + 'Ticket/Display.html?id='
        rt=RT(rtuser,rtpassword,rt_rest_url,self.logger)	
	report=['id','subject','message']
        report_list=[]
	rt_action=self.parameters.action

	try:
      	    current_id_str=open(self.parameters.cur_id_filelocation+self.bot_id,'r').read()
	    current_id=int(current_id_str)
        except:
            current_id=None

	

	
        if current_id:
	   self.logger.info("Downloading reports from RT ID %d" % current_id)	
           reports=rt.get_ids_and_titles_reports_by_subject(current_id,subject_filter)
        else:
	   self.logger.info("Downloading reports from RT ID %d" % from_id)
           reports=rt.get_ids_and_titles_reports_by_subject(from_id,subject_filter)
	if reports:
         if not reports[0].startswith('No matching results.') and not reports[0].startswith('Your username or password is incorrect'):
            open(self.parameters.cur_id_filelocation+self.bot_id,'w').write(reports[len(reports)-1].split(':')[0])
	    for r in reports:
	        values=[]
	        ticketid=r.split(':')[0]
                values.append(r.split(':')[0])
	        values.append(r.split(':')[1])
	        larger_report=""
	        for attachment in rt.get_text_attachments(r.split(':')[0]):
                    if len(attachment)>len(larger_report):
	 	      larger_report=attachment  
                values.append(larger_report)
	        report_list.append(dict(zip(report,values)))  
	        if rt_action=='reject':  
	           rt.reject_report(ticketid)
	        if rt_action=='resolve':
	           rt.resolve_ticket(ticketid, reason=None)
            self.logger.info("Reports downloaded.")
	    self.logger.info(report_list) 	
            self.send_message(report_list)


if __name__ == "__main__":
    bot = RTCollectorBot(sys.argv[1])
    bot.start()
