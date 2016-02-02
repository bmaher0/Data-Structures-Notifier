import datetime, time, check_helper


def main(cycles, delay):
	current_max = -1
	for i in range(cycles):
		print "%s #%d" % (datetime.datetime.now(), i)
		if check_helper.should_countinue():
			old_assigns = check_helper.read_assignments()
			current_assigns = check_helper.get_assignments()
			new_assigns = current_assigns - old_assigns
			if new_assigns == set():
				print "No new assignments"
			else:
				print "New assignments: %s" % (list(new_assigns))
				check_helper.write_assignments(current_assigns)
			time.sleep(delay)
		else:
			return False
	return True

if __name__ == "__main__":
	cycles = 10
	delay = 10
	main(cycles, delay)