import smtplib, imaplib, html_helper, sys
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText


config_path = "account_config.txt"
recip_path = "recip_list.txt"

sig_file = r"msgs\sig.txt"
welcome_file = r"msgs\welcome.txt"
notif_file = r"msgs\notif.txt"
remove_file = r"msgs\remove.txt"
noncommand_file = r"msgs\noncommand.txt"

def read_signature():
	return open(sig_file, 'r').read()

def read_msg_template(filename):
	contents = open(filename, 'r').readlines()
	if len(contents) < 2:
		print "ERROR bad message template: %s" % filename
		sys.exit(1)
	else:
		subject = contents[0].strip()
		message = ''.join(contents[1:]) + read_signature()
		return subject, message

def read_recip_set():
	try:
		return eval(open(recip_path, 'r').read())
	except:
		print "ERROR: %s not found." % recip_path
		while True:
			response = raw_input("Retry? (Y/N) ")
			if response == "Y":
				return read_recip_set()
			elif response == "N":
				while True:
					response = raw_input("Create new empty recipient list? If N then the system will exit. (Y/N) ")
					if response == "Y":
						write_recip_set(set())
						return set()
					elif response == "N":
						print "Exiting."
						sys.exit(1)
					else:
						print "Invalid command."
			else:
				print "Invalid command."

def write_recip_set(recip_set):
	open(recip_path, 'w').write(repr(recip_set))

def login(server):
	username = ""
	password = ""
	found = False
	try:
		file_data = open(config_path).readlines()
		username = file_data[0].strip()
		password = file_data[1].strip()
		found = True
	except IOError:
		print 
	while True:
		try:
			server.login(username, password)
			break;
		except imaplib.IMAP4.error:
			if found:
				print "Invalid username or password." 
			else:
				print "%s not found." % config_path 
			response = raw_input("Input new username and password? (Y/N) ")
			if response == "Y":
				username = raw_input("New gmail address (including @gmail.com): ")
				password = raw_input("New password: ")
				f = open(config_path, 'w')
				f.write(username + '\n' + password)
				f.close()
			else:
				print "Exiting."
				sys.exit(1)
	return username

def send_mail(to_address, subject, msg_text):
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	username = login(server)

	msg = MIMEMultipart()
	msg['From'] = username
	msg['To'] = to_address
	msg['Subject'] = subject
	msg.attach(MIMEText(msg_text, 'plain'))

	server.sendmail(username, to_address, msg.as_string())
	server.quit()

def send_mail_list(subject, msg_text, address_set):
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	username = login(server)

	for to_address in address_set:
		msg = MIMEMultipart()
		msg['From'] = username
		msg['To'] = to_address
		msg['Subject'] = subject
		msg.attach(MIMEText(msg_text, 'plain'))
		print "-Sending message to %s" % to_address
		server.sendmail(username, to_address, msg.as_string())
	
	server.quit()

def get_addresses_update():
	add, remove, other = set(), set(), set()

	server = imaplib.IMAP4_SSL('imap.gmail.com', 993)
	login(server)
	server.select("INBOX")
	result, data = server.search(None, "ALL")
	if result == "OK":
		if len(data[0].split()) > 0:
			print "*Commands received:"
		else:
			print "*No commands received"
		for num in data[0].split():
			result, fetched_data = server.fetch(num, "(BODY[HEADER.FIELDS (SUBJECT FROM)])")
			fetched_data_list = fetched_data[0][1].split("\r\n")

			from_info = ""
			subject = ""

			for value in fetched_data_list:
				if "From: " in value:
					from_info = value.replace("From:", "", 1).strip()
				elif "Subject: " in value:
					subject = value.replace("Subject:", "", 1).strip()

			command = subject.lower()
			print from_info
			from_address = from_address_helper(from_info)
			print '-%s: "%s"' % (from_address, subject)

			if "subscribe" in command and not "un" in command:
				add.add(from_address)
			elif "unsubscribe" in command:
				remove.add(from_address)
			else:
				other.add(from_address)
			server.store(num, '+FLAGS', '\\Deleted')
	else:
		pass
		#this will be an error of some sort
	return add, remove, other

def update_subscriptions():
	add, remove, other = get_addresses_update()
	recip_set = read_recip_set()

	if len(add) > 0:
		welcome_sub, welcome_msg = read_msg_template(welcome_file)
		print "*Subscribing:"
		send_mail_list(welcome_sub, welcome_msg, add)
		recip_set = recip_set | add
	if len(remove) > 0:
		remove_subject, remove_message = read_msg_template(remove_file)
		print "*Unsubscribing:"
		send_mail_list(remove_subject, remove_message, remove)
		recip_set = recip_set - remove
	if len(other) > 0:
		nc_subject, nc_message = read_msg_template(noncommand_file)
		print "*Non-command notification:"
		send_mail_list(nc_subject, nc_message, other)
	write_recip_set(recip_set)

def notify_assignment(assign):
	notif_subject, notif_message = read_msg_template(notif_file)
	print "**Assignment: %s" % assign
	subject = notif_subject % assign
	msg_text = notif_message % (assign, html_helper.short_cal_url)
	send_mail_list(subject, msg_text, read_recip_set())

def from_address_helper(from_info):
	if "<" in from_info:
		addr_begin = from_info.find("<")
		addr_end = from_info.find(">")
		return from_info[addr_begin+1:addr_end]
	return from_info

if __name__ == "__main__":
	update_subscribers()