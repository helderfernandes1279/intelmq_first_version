import cookielib
import urllib
import urllib2
import re


class RT():
    
    def __init__(self, username, password, base_url,logger):
        self.username = username
        self.password = password
        self.base_url = base_url
	self.logger=logger
    def get_url(self, url, content=None):
        import time
        continua = 0
        toRet = ""
        while continua < 4:
            try:
                toRet = self._get_url(url, content)
                continua = 5
            except Exception, e:
                self.logger.info('RT Connection failed - %r' % e)
                continua += 1
                time.sleep(30)

        return toRet

    def _get_url(self, url, content=None):
        urllib.urlcleanup()
        headers = {"Accept": "text/plain"}
        rest = self.base_url
        user = self.username
        passwd = self.password
        
        if not rest or not user or not passwd:
            self.logger.info("Could contact RT, bad or missing args (host: %s user: %s or passwd)", rest, user)
            return u""

        cj = cookielib.LWPCookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)
        if content is None:
            data = {'user': user, 'pass': passwd}
        else:
            data = {'user': user, 'pass': passwd, 'content': content}

        #self.log.info("Data to be sent by RT:\n%r", data)
        ldata = urllib.urlencode(data)
        uri = rest + url
        login = urllib2.Request(uri, ldata)

        response_data = ""
        try:
            response = urllib2.urlopen(login)
            response_data = response.read()

            self.logger.info("RT Connection successful: %r", response_data)
        except urllib2.URLError, exc:
            # could not connect to server
            self.logger.info("RT Connection failed: %r", exc)

        return response_data

    def get_ids_and_titles_reports_by_subject(self, from_id,subject):
        url = "search/ticket?query=id>" + str(from_id) + "%20AND%20(%20'CF.%7B_RTIR_State%7D'%20%3D%20'new'%20OR%20'CF.%7B_RTIR_State%7D'%20%3D%20'open'%20)%20AND%20(Subject%20LIKE%20'"+subject.replace(' ','%20')+"')%20AND%20MemberOf%20IS%20NULL%20AND%20Queue%20%3D%20'Incident%20Reports'&orderby=Id&format=s"
	
	response_data = self.get_url(url)
	ir_list = list()
	response=response_data.splitlines()
        for line in response[1:]:
          if line is not None and line!='':
             ir_list.append(line)
	      
        return ir_list

   

    def get_text_attachments(self, ticket_id):
        attach_list = self.get_attachment_list(ticket_id)
	attachments = list()
        for attach in attach_list:
            if re.search('text/', attach['type']) is not None:
                text = self.get_attachment_content(ticket_id, attach['id'])
                attachments.append(text)

        return attachments

    def get_attachment_list(self, ticket_id):
        url = "ticket/" + ticket_id + "/attachments"
        data = self.get_url(url);
        attachs = [m.groupdict() for m in re.finditer("(?P<id>\d+): ((?P<name>.*?)|\(Unnamed\)) \((?P<type>.*?)\).*", data)]

        return attachs

    def get_attachment_headers(self, ticket_id, attach_id):
        url = "ticket/" + ticket_id + "/attachments/" + attach_id
        data = self.get_url(url);

        match = re.findall('Headers: (.*)\n(\S|$)', data, re.MULTILINE | re.DOTALL)

        if len(match) > 0:
            return match[0][0].strip()
        else:
            return ''

    def get_attachment_content(self, ticket_id, attach_id):
        url = "ticket/" + ticket_id + "/attachments/" + attach_id
        data = self.get_url(url);

        match = re.findall('Content: (.*)\n(\S|$)', data, re.MULTILINE | re.DOTALL)

        if len(match) > 0:
            return match[0][0].strip()
        else:
            return ''

    def edit_ticket(self, id, content):
        return self.get_url('ticket/' + str(id) + '/edit', content)

    def resolve_ticket(self, ticket_id, reason=None):
        content = 'Status: resolved\n'
        content += 'CF.{_RTIR_State}: resolved\n'
        content += 'Owner: ' + self.username

        if reason is not None and ticket.__class__.__name__ == 'Incident':
            content += 'CF.{_RTIR_Resolution}: ' + reason
        self.edit_ticket(ticket_id, content)


    def reject_report(self, ticket_id):
        content = 'Status: rejected\n'
        content += 'CF.{_RTIR_State}: rejected\n'
        content += 'Owner: ' + self.username
	self.edit_ticket(ticket_id, content)
