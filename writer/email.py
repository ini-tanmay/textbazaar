import smtplib

server=smtplib.SMTP('smtp.mailgun.org', 587)
server.ehlo()
server.starttls()
server.login('postmaster@mail.sochial.media', '4f99da1a15d62b6ba6db756c117cc541-1f1bd6a9-c5600578')

def send_email(article,email):    
    article="Subject: Hey! your new AI generated blog post -\n\n"+article
    server.sendmail('postmaster@mail.sochial.media', email, article.encode('utf-8'))
    # server.close()