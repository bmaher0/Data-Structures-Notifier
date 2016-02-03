import datetime, time, check_helper, gmail_helper, sys

# cycles is the number of cycles to iterate through before terminating
# delay is the delay (in seconds) between each cycle
def main(cycles, delay):
	for i in range(cycles):
		# print time stamp and cycle number
		print "%s #%d" % (datetime.datetime.now(), i)
		# if the escape file is not fould
		if check_helper.should_countinue():
			# check for new subscribes/unsubscribes and do that
			gmail_helper.update_subscriptions()
			# create a set for new assignments and a set of all current assignments
			new_assigns, current_assigns = check_helper.new_assignments()
			# if the new assignment set is empty
			if new_assigns == set():
				print "-No new assignments"
			# if there are new assignments
			else:
				print "-New assignments: %s" % new_assigns
				#for each new assignment, send out an email notification
				for assign in new_assigns:
					gmail_helper.notify_assignment(assign)
				#update the assignment cache file
				check_helper.write_assignments(current_assigns)
		# if the escape program is found, return False which will exit the loop
		else:
			print "Escape file detected, exiting program."
			return False
		# delay between cycles
		time.sleep(delay)
	return True

if __name__ == "__main__":
	# default values for cycles and delays
	cycles = 4
	delay = 5
	# if there are two command line arguments, use them to set cycles and delay
	if len(sys.argv) == 3:
		#set the cycles and delay, or exit if there is a ValueError
		try:
			cycles = int(sys.argv[1])
			delay = int(sys.argv[2])
		except ValueError:
			print "ERROR: arguments are not both positive integers."
			sys.exit(1)
	#if there are no command line arguments, pass which will use default 
	# cycle and delay
	elif (len(sys.argv) == 1):
		pass
	# if there are any other number of arguments, throw an error and exit
	else:
		print "ERROR: incorrect number of arguments:",
		print "2 expected, %d given." % (len(sys.argv)-1)
		sys.exit(1)

	#if the cycles are positive integers, run the main
	if cycles > 0 and delay > 0:
		main(cycles, delay)
	#if they are not positive integers, throw an error and exit
	else:
		print "ERROR: arguments are not both positive integers."
		sys.exit(1)