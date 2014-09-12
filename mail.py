import sys
import os
import re
from smtplib import SMTP
import email.mime.text
import datetime

class Mailer():
	def __init__(self):
		self.eventlist = []
		self.foldername = 'C:/ION_Mail'
		self.event = 0
		self.timestamp = 1
		self.datetime = None
		self.SMTPserver = None
		self.sender = None
		self.text_subtype = 'html' # plain, html, xml
		self.destination = []
		self.body = ""
		self.gmt = 0
		self.config = ''
		self.config_file = ''
		self.config_msg = ''
		self.is_test = False

# sys.argv = [ exe name , param 1 (eventcode), param 2 (timestamp), param 3 (substation config file)]
	def ParseGetVars(self):
		self.foldername = os.path.dirname(str(sys.argv[0]))
		if len(sys.argv)<4:
			self.is_test = True
		else:
			self.event = str(sys.argv[1])
			self.event = self.event[0:-3]
			self.timestamp = str(sys.argv[2])
			self.timestamp = self.timestamp[0:-3]
			self.config = str(sys.argv[3])
			self.config_file = self.foldername + '/m_serverconfig_'+self.config+'.txt'
			self.config_msg = self.foldername + '/m_message_'+self.config+'.txt'

	def OpenConfigFile(self):
		mailfile = []
		with open(self.config_file, 'r') as f:
			for line in f.readlines():
				if line[0:1]!="#":
					mailfile.append(line[0:-1])
# mailfile = [ IP smtp server , sender name, subject, mailto ]
		dest = mailfile[3].split(",")
		for item in dest:
			self.destination.append(item.strip())
		self.SMTPserver = mailfile[0]
		self.sender = mailfile[1]
		self.subject = mailfile[2]
		self.gmt = mailfile[4]

	def OpenMessageFile(self):
		with open(self.config_msg, 'r') as f:
			for line in f.readlines():
				self.eventlist.append(line[0:-1])

# Convert timestamp utc to date time
	def TimestampConvert(self):
		self.timestamp = int(self.timestamp) + int(self.gmt)*60
		self.datetime = datetime.datetime.fromtimestamp(int(self.timestamp)).strftime('%Y-%m-%d %H:%M:%S')

	def SelectEvent(self, code, eventlist):
		if code.isdigit()==True:
			if not eventlist[int(code)]:
				self.event= "No event found in list"
			else:
				self.event = eventlist[int(code)]
		else:
			self.event = "No event found"

	def OpenBodyFile(self):
		with open(self.foldername + '/m_body.html', 'r') as f:
			for line in f.readlines():
				self.body += line
		self.body=self.body.replace("$event$", self.event)
		self.body=self.body.replace("$datetime$", self.datetime)

	def MainMail(self, test=False):
		self.ParseGetVars()
		if self.is_test == True:
			content_test = """
			<html><body>
			*** TEST MAIL, it Works!! ***
			<br><br><br>
			Engels Rodriguez<br>
			Servicios Avanzados<br>
			<b>Schneider Electric Peru - 2014</b>
			</body></html>
			"""
			msg = email.mime.text.MIMEText(content_test, self.text_subtype)
		else:
			self.OpenConfigFile()
			self.OpenMessageFile()
			self.TimestampConvert()
			self.SelectEvent(str(self.event), self.eventlist)
			self.OpenBodyFile()
			msg = email.mime.text.MIMEText(self.body, self.text_subtype)
		msg['Subject']= self.subject + ' ' + self.event
		msg['From']   = self.sender
		conn = SMTP(self.SMTPserver)
		conn.set_debuglevel(False)
		#conn.login(USERNAME, PASSWORD)
		conn.sendmail(self.sender, self.destination, msg.as_string())
		conn.close()

try:
	mail = Mailer()
	mail.MainMail()
except Exception,e:
	f=open('C:/ION_Mail/error.txt','a')
	f.write(str(e))
	f.close()
