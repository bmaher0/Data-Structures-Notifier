import datetime, time, check_helper

def main(cycles, delay):
	current_max = -1
	for i in range(cycles):
		print "%s #%d" % (datetime.datetime.now(), i)
		if check_helper.should_countinue():
			current_max = check_helper.check(current_max)
			time.sleep(delay)
		else:
			return False
	return True

if __name__ == "__main__":
	cycles = 100
	delay = 2
	main(cycles, delay)