import datetime, time, check_helper, gmail_helper, sys


def main(cycles, delay):
	for i in range(cycles):
		print "%s #%d" % (datetime.datetime.now(), i)
		if check_helper.should_countinue():
			new_assigns, current_assigns = check_helper.new_assignments()
			if new_assigns == set():
				print "-No new assignments"
			else:
				print "-New assignments: %s" % (new_assigns)
				for assign in new_assigns:
					gmail_helper.notify_assignment(assign)
				check_helper.write_assignments(current_assigns)
		else:
			return False
		time.sleep(delay)
	return True

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print "ERROR: not enough arguments."
		sys.exit(1)
	else:
		cycles = int(sys.argv[1])
		delay = int(sys.argv[2])
		main(cycles, delay)