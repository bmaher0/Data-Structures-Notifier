import datetime, time, check_helper, gmail_helper, html_helper


def main(cycles, delay):
	for i in range(cycles):
		print "%s #%d" % (datetime.datetime.now(), i)
		if check_helper.should_countinue():
			new_assigns, current_assigns = check_helper.new_assignments()
			if new_assigns == set():
				print "No new assignments"
			else:
				print "New assignments: %s" % (list(new_assigns))
				check_helper.write_assignments(current_assigns)
				for assign in new_assigns:
					subject = "New Data Structures assignment: %s" % assign
					msg_text = "A new Data Structures assignment, %s, has been posted to the calendar: %s" % (assign, html_helper.calendar_url)
					gmail_helper.send_mail_list(gmail_helper.recip_path, subject, msg_text)
		else:
			return False
		time.sleep(delay)
	return True

if __name__ == "__main__":
	cycles = 2
	delay = 5
	main(cycles, delay)