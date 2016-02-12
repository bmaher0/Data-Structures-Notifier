import datetime, smtplib, imaplib, html_helper, sys
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

# location of gmail login/password
config_path = "account_config.txt"
# location of mailing list, stored as the string representation of a python set
recip_path = "recip_list.txt"

# locations of various message templates
# signature, appended to all outgoing messages
sig_file = "msgs/sig.txt"
# message for new subscribers
welcome_file = "msgs/welcome.txt"
# template for assignment notification
notif_file = "msgs/notif.txt"
# message for unsubscribers
remove_file = "msgs/remove.txt"
# message to respond to invalid commands
noncommand_file = "msgs/noncommand.txt"
# message to respond to test command
test_file = "msgs/test.txt"
# response to subscribe request when already subscribed
already_add_file = "msgs/already_add.txt"
# response to unsubscribe request when not subscribed
already_rem_file = "msgs/already_rem.txt"

# reads signature from file
def read_signature():
	return open(sig_file, 'r').read()

# constructs a message string from a template file given by filename
# returns tuple of (subject, message)
def read_msg_template(filename, signature=True):
	contents = open(filename, 'r').readlines()
	#if there are fewer than two lines, then the template isn't valid
	if len(contents) < 2: 
		print "ERROR bad message template: %s" % filename
		sys.exit(1)
	else:
		#join the lines together, append signature if signature == True
		subject = contents[0].strip()
		message = ''.join(contents[1:])
		if signature:
			message += read_signature()
		return subject, message

def read_recip_set():
	# open the file, if successful return the recipient set
	try:
		return eval(open(recip_path, 'r').read())
	# if the file is not found
	except IOError:
		print "ERROR: %s not found." % recip_path
		while True:
			# offer to try again
			response = raw_input("Retry? (Y/N) ")
			if response == "Y":
				# try again, recursively
				return read_recip_set()
			elif response == "N":
				while True:
					# ask the user if it wants to create a new recipient file
					response = raw_input("Create new empty recipient list? If N then the system will exit. (Y/N) ")
					if response == "Y":
						# write empty reicipient set
						write_recip_set(set())
						# return an empty set
						return set()
					elif response == "N":
						print "Exiting."
						sys.exit(1)
					else:
						print "ERROR invalid command."
			else:
				print "ERROR invalid command."

# write new recipient set
def write_recip_set(recip_set):
	open(recip_path, 'w').write(repr(recip_set))

# log in to the server, which can be represented as an smtplib.SMTP or imaplib.IMAP4 object
def login(server):
	username = ""
	password = ""
	found = False
	# try to load the username and password from config_path
	try:
		file_data = open(config_path).readlines()
		username = file_data[0].strip()
		password = file_data[1].strip()
		found = True
	# pass if a file is not found
	except IOError:
		pass
	while True:
		# try to log in, break if successful
		try:
			server.login(username, password)
			break;
		#if log in fails
		except imaplib.IMAP4.error:
			if found:
				print "Invalid username or password." 
			else:
				print "%s not found." % config_path 
			# ask if it should take input for new username and password
			response = raw_input("Input new username and password? (Y/N) ")
			if response == "Y":
				# take input for username and password
				username = raw_input("New gmail address (including @gmail.com): ")
				password = raw_input("New password: ")
				#write new config file
				f = open(config_path, 'w')
				f.write(username + '\n' + password)
				f.close()
			else:
				print "Exiting."
				sys.exit(1)
	return username

def send_mail(to_address, subject, msg_text):
	# log into the email server
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	username = login(server)

	# structure message details into MIMEMultipart message
	msg = MIMEMultipart()
	msg['From'] = username
	msg['To'] = to_address
	msg['Subject'] = subject
	msg.attach(MIMEText(msg_text, 'plain'))

	# send the message and quit
	server.sendmail(username, to_address, msg.as_string())
	server.quit()

# send mail to a set of email addresses
def send_mail_list(subject, msg_text, address_set):
	# log into the email server
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	username = login(server)

	for to_address in address_set:
		# structure message details into MIMEMultipart message
		msg = MIMEMultipart()
		msg['From'] = username
		msg['To'] = to_address
		msg['Subject'] = subject
		msg.attach(MIMEText(msg_text, 'plain'))

		# send message
		print "-Sending message to %s" % to_address
		server.sendmail(username, to_address, msg.as_string())
	server.quit()

# scrape the email server to get sets to add to the list, remove from the list, 
# send test notifications, and non-command responses
def get_addresses_update():
	add, remove, test, other = set(), set(), set(), set()
	# connect to the server
	server = imaplib.IMAP4_SSL('imap.gmail.com', 993)
	login(server)
	#open the inbox and search it
	server.select("INBOX")
	result, data = server.search(None, "ALL")
	# if the request went through
	if result == "OK":
		if len(data[0].split()) > 0:
			print "*Commands received:"
		else:
			print "*No commands received"
		# for each message in the inbox
		for num in data[0].split():
			# fetch the message from the inbox
			result, fetched_header_data = server.fetch(num, "(BODY[HEADER.FIELDS (SUBJECT FROM)])")# #BODY[TEXT])")
			result, fetched_body_data = server.fetch(num, "(BODY[TEXT])")
			fetched_header_list = fetched_header_data[0][1].split("\r\n")
			body_string = fetched_body_data[0][1].split("\r\n\r")[0]

			from_info = ""
			subject = ""

			# find the from address and subject in the email
			for value in fetched_header_list:
				if "From: " in value:
					from_info = value.replace("From:", "", 1).strip()
				elif "Subject: " in value:
					subject = value.replace("Subject:", "", 1).strip()

			command = (subject + body_string).lower()
			print from_info
			from_address = from_address_helper(from_info)
			print '-%s: "%s"' % (from_address, subject)

			# evaluate the command and sort the sender into the appropriate set
			if "subscribe" in command and not "un" in command:
				add.add(from_address)
			elif "unsubscribe" in command:
				remove.add(from_address)
			elif "test" in command:
				test.add(from_address)
			else:
				other.add(from_address)

			# delete the email
			server.store(num, '+FLAGS', '\\Deleted')
	else:
		pass
		# this will be an error of some sort if the email request doesn't go through
	return add, remove, test, other

def update_subscriptions():
	add, remove, test, other = get_addresses_update()
	recip_set = read_recip_set()

	# create a set of users attempting to be added when they're already on the list
	add_already = add & recip_set 
	add = add - add_already

	# create a set of users attempting to be removed when they're not on the list
	remove_already = remove - recip_set
	remove = remove - remove_already

	# add all users not yet on the list
	if len(add) > 0:
		welcome_sub, welcome_msg = read_msg_template(welcome_file)
		print "*Subscribing:"
		send_mail_list(welcome_sub, welcome_msg, add)
		recip_set = recip_set | add

	# notify all users who want to be added but are already on it
	if len(add_already) > 0:
		already_add_sub, already_add_msg = read_msg_template(already_add_file)
		print "*Already subscribed:"
		send_mail_list(already_add_sub, already_add_msg, add_already)

	# remove all users on the list
	if len(remove) > 0:
		remove_subject, remove_message = read_msg_template(remove_file)
		print "*Unsubscribing:"
		send_mail_list(remove_subject, remove_message, remove)
		recip_set = recip_set - remove

	# notify all the users that want to be removed and aren't on the list
	if len(remove_already) > 0:
		alr_rem_sub, alr_rem_msg = read_msg_template(already_rem_file)
		print "Not subscribed:"
		send_mail_list(alr_rem_sub, alr_rem_msg, remove_already)

	# notify all users who sent invalid commands
	if len(other) > 0:
		nc_subject, nc_message = read_msg_template(noncommand_file)
		print "*Non-command notification:"
		send_mail_list(nc_subject, nc_message, other)
	
	# respond to all test requests
	if len(test) > 0:
		test_subject, test_message = read_msg_template(test_file, signature=False)
		print "*Responding to test request:"
		send_mail_list(test_subject, test_message % datetime.datetime.now(), test)
	write_recip_set(recip_set)

# send assignment notification messages
def notify_assignment(assign):
	# read message info from the template
	notif_subject, notif_message = read_msg_template(notif_file)
	print "**Assignment: %s" % assign
	# string format with the assignment name
	subject = notif_subject % assign
	msg_text = notif_message % (assign, html_helper.short_cal_url)
	# send message
	send_mail_list(subject, msg_text, read_recip_set())

# parse the from info in emails and get the sender's address
def from_address_helper(from_info):
	if "<" in from_info:
		addr_begin = from_info.find("<")
		addr_end = from_info.find(">")
		return from_info[addr_begin+1:addr_end]
	return from_info

if __name__ == "__main__":
	update_subscribers()