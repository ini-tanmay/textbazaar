import smtplib, ssl

port = 465  # For SSL

# Create a secure SSL context
# context = ssl.create_default_context()

# with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
#     server.login("b2bneedz@gmail.com", 'b2bneedz123')
#     # TODO: Send email here
server = smtplib.SMTP_SSL()

def send_email(article,email):    
    server.login('postmaster@mail.sochial.media', '4f99da1a15d62b6ba6db756c117cc541-1f1bd6a9-c5600578')
    article="Subject: Hey!, your new AI generated blog post -\n\n"+article
    server.sendmail('postmaster@mail.sochial.media', email, article.encode('utf-8'))
