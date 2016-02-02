import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

config_path = "C:/ds_notif/account_config.txt"
recip_path = "C:/ds_notif/recip_list.txt"

def send_mail(to_address, subject, msg_text):
	file_data = open(config_path).readlines()
	username = file_data[0].strip()
	password = file_data[1].strip()

	msg = MIMEMultipart()
	msg['From'] = username
	msg['To'] = to_address
	msg['Subject'] = subject
	msg.attach(MIMEText(msg_text, 'plain'))

	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(username, password)
	server.sendmail(username, to_address, msg.as_string())
	server.quit()

def send_mail_list(filename, subject, msg_text):
	for line in open(filename):
		address = line.strip()
		print repr(address)
		send_mail(address, subject, msg_text)

if __name__ == "__main__":
	send_mail("brianmaher529@gmail.com", "test", "eyyyyoo!")