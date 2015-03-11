# EmailModel.py
import smtplib
from env_config import SMTPSERVER, SMTPPORT, FROMEMAIL, FROMPASS


class EmailModel:

    def __init__(self):
        pass

    def send_one_email(self,to,subject,content):
           
        #server = smtplib.SMTP('smtp.gmail.com', 587)
        print('FLAGX0 send_one_email')

        server = smtplib.SMTP(SMTPSERVER,SMTPPORT)
        
        print('FLAGX1',server,SMTPSERVER,SMTPPORT)
        server.ehlo()
        print('FLAGX2')
        server.starttls()
        print('FLAGX3',FROMEMAIL, FROMPASS)

        #Next, log in to the server
        server.login(FROMEMAIL, FROMPASS)

        print('FLAGX4')

        #Send the mail
        msg = "\r\n".join([
          "From:"+FROMEMAIL,
          "To: "+to,
          "Subject: "+subject,
          "",
          content
          ])
        #msg = "\nHello!" # The /n separates the message from the headers

        print('FLAGX5')

        server.sendmail(FROMEMAIL, to, msg)
        print('FLAGX6')
        server.quit()
        print('FLAGX7')

        print(msg)
        print("Sending email to: "+to)

        return True


