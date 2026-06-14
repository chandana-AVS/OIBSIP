import smtplib

sender_email = "avschandana@gmail.com"
app_password = "zcvhxhhuyiswfesn"

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()

server.login(sender_email, app_password)

print("LOGIN SUCCESS")