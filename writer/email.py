from django.core.mail import send_mail
# import smtplib

# server=smtplib.SMTP('smtp.mailgun.org', 587)
# # server.ehlo()
# server.starttls()
# server.login('postmaster@mail.sochial.media', '4f99da1a15d62b6ba6db756c117cc541-1f1bd6a9-c5600578')

def send_email(subject,article,email):    
    # article="Subject: Hey! your new AI generated blog post -\n\n"+article
    print(article)
    print(type(article))
    send_mail(subject, article, 'postmaster@mail.sochial.media', [email])
    # server.sendmail('postmaster@mail.sochial.media', email, article.encode('utf-8'))
    # server.close()

# API_KEY = 'e8e4946671359555288ecc0113d48769-aff8aa95-60f73cc8'
# YOUR_DOMAIN_NAME= "mail.sochial.media"

# def send_email_2(article,email):
#         return requests.post(
#             f"https://api.mailgun.net/v3/",
#             auth=("api", API_KEY),
#             data={"from": f"Excited User <mailgun@{YOUR_DOMAIN_NAME}",
#                   "to": ["tanmay.armal@somaiya.edu"],
#                   "subject": "Hello",
#                   "text": "Testing some Mailgun awesomness!"})
