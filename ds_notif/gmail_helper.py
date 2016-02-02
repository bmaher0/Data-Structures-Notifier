import smtplib

config_path = "C:/ds_notif/account_config.txt"

def sendMail(to_address, msg_text):
	file_data = open(config_path).readlines()
	username = file_data[0].strip()
	password = file_data[1].strip()

	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(username, password)
 
	server.sendmail(username, to_address, msg_text)
	server.quit()

if __name__ == "__main__":
