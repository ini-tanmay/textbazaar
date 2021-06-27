import smtplib, ssl

port = 465  # For SSL

# Create a secure SSL context
# context = ssl.create_default_context()

# with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
#     server.login("b2bneedz@gmail.com", 'b2bneedz123')
#     # TODO: Send email here
server = smtplib.SMTP_SSL('smtp.googlemail.com', port)
server.login('b2bneedz@gmail.com', 'b2bneedz123')

def send_email(article):    
    article="Subject: Hi there\n\n"+article
    server.sendmail('b2bneedz@gmail.com', 'tanmay.armal@somaiya.edu', article.encode(utf-8))
