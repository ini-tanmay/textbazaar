import smtplib, ssl

port = 465  # For SSL

# Create a secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login("b2bneedz@gmail.com", 'b2bneedz123')
    # TODO: Send email here

def send_email(article):    
    server.sendmail('b2bneedz@gmail.com', 'tanmay.armal@somaiya.edu', article)
