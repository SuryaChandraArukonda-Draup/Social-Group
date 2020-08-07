import smtplib


# list of email_id to send the mail
# recipients = ["xxxxx@gmail.com", "yyyyy@gmail.com"]

def send_mail(recipients, content):
    for mail in recipients:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login("suryachandraarukonda16@gmail.com", "coolchandraA@1")
        s.sendmail("suryachandraarukonda16@gmail.com", mail, content)
        s.quit()
