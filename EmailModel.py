# EmailModel.py
import smtplib
from env_config import FROMEMAIL, FROMPASS


class EmailModel:

    def __init__(self):
        pass

    def send_one_email(self,to,subject,content):
           
        #server = smtplib.SMTP('smtp.gmail.com', 587)
        server = smtplib.SMTP('smtp.sendgrid.net', 587)
        server.ehlo()
        server.starttls()

        #Next, log in to the server
        server.login(FROMEMAIL, FROMPASS)

        #Send the mail
        msg = "\r\n".join([
          "From:"+FROMEMAIL,
          "To: "+to,
          "Subject: "+subject,
          "",
          content
          ])
        #msg = "\nHello!" # The /n separates the message from the headers
        server.sendmail(FROMEMAIL, to, msg)
        server.quit()

        print(msg)
        print("Sending email to: "+to)