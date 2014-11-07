# MyRingEmailer.py
import smtplib

sender = 'rcid@myring.io'
receivers = ['ricardo@blacklabelrobot.com']

message = """From: From Person <rcid@myring.io>
To: To Person <ricardo@blacklabelrobot.com>
Subject: SMTP e-mail test

This is a test e-mail message.
"""

try:
   smtpObj = smtplib.SMTP('localhost')
   smtpObj.sendmail(sender, receivers, message)         
   print "Successfully sent email"
except SMTPException:
   print "Error: unable to send email"