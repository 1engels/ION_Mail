import sys
import os
import re
from smtplib import SMTP
import email.mime.text
import datetime

class Mailer():
	def __init__(self):
		self.eventlist = []
		self.event = None
		self.timestamp = ""
		self.datetime = None
		self.SMTPserver = None
		self.sender = None
		self.text_subtype = 'html' # typical values for text_subtype are plain, html, xml
		self.destination = []
		self.body = ""

# sys.argv = [ exe name , param 1 (eventcode), param 2 (timestamp)]
	def ParseGetVars(self):
		self.event = str(sys.argv[1])
		self.timestamp = str(sys.argv[2])
		#self.event = "1"
		#self.timestamp = "1381463561"

	def OpenConfigFile(self):
		mailfile = []
		with open('m_serverconfig.txt', 'r') as f:
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
		if mailfile[3].isdigit() == True:
			self.gmt = mailfile[3]
		else:
			self.gmt=0

	def OpenMessageFile(self):
		with open("m_message.txt", 'r') as f:
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
		with open("m_body.html", 'r') as f:
			for line in f.readlines():
				self.body += line
		self.body=self.body.replace("$event$", self.event)
		self.body=self.body.replace("$datetime$", self.datetime)

	def MainMail(self, test=False):
		self.ParseGetVars()
		self.OpenConfigFile()
		self.OpenMessageFile()
		self.TimestampConvert()
		self.SelectEvent(self.event, self.eventlist)
		self.OpenBodyFile()
		content=self.body
		content_test = """
		<html><body>
		MEDIDOR ION
		<br><br>
		*** TESTING MAIL, it Works!! ***
		<br><br><br>
		Servicios Avanzados
		Schneider Electric Peru - 2013
		</body></html>
		"""
		'''
		print self.body
		print self.event
		print self.datetime
		print self.destination
		print self.sender
		print self.SMTPserver
		print self.eventlist
		'''
		if test==False:
			msg = email.mime.text.MIMEText(content, self.text_subtype)
		else:
			msg = email.mime.text.MIMEText(content_test, self.text_subtype)
		msg['Subject']= self.subject + ' ' + self.event
		msg['From']   = self.sender

		conn = SMTP(self.SMTPserver)
		conn.set_debuglevel(False)
		#conn.login(USERNAME, PASSWORD)
		conn.sendmail(self.sender, self.destination, msg.as_string())
		conn.close()
		
mail = Mailer()
mail.MainMail()
