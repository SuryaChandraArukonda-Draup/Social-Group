import smtplib


def send_email(mail, content):
    server = smtplib.SMTP('smtp.gmail.com', 27017)
    server.starttls()
    server.login("emailid", "password")
    server.sendmail("senders email", mail, content)
    server.quit()
