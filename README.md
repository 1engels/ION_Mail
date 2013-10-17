ION_mail
========

This is a program used for sending mails using launching module in ION Enterprise or PME.

It takes three external files to work.

1.- m_body.html

This file contains the body of the mail, for a better presentation it must be an html file, so we can customize it.

2.- m_message.txt

This file contains the list of messages that can be desplayed on the message related to some given event.

3.- m_serverconfig.txt

This file contains the server configuration values like SMTP Server IP, sender name, destination list and Timezone
(Use GMT 0 if your linking localtime from clock module)


CALLING THE PROGRAM FROM Launching Module
=========================================

Link two inputs to Launching Module:

1. Event: This is a numeric value, it is the event code to search in the m_message.txt

2. Timestamp: This is a numeric value, it represents the value in seconds since 1st Jan 1970


SAMPLE
======

(You can convert mail.py to mail.exe using py2exe)

Put the 4 files into this directory: C:/ION_Mail

Configure m_serverconfig.txt with your server data and leave GMT 0 (Clock module sends local time)

Also Launching module with Run Command setup variable: 

python C:/ION_Mail/mail.py 1 1381674592

Run it! You'll get a mail saying:

Trip reason: 1st Stage - Freq min

Trip time: 10/13/2013 09:29:52

Enjoy it!
If you have more ideas just feel free to contact me.
