import html_helper

# if there is a text file called "stop.txt" in the program directory,
# the script will stop running at the beginning of the next cycle
escape_file = "stop.txt"
assignment_file = "assign_cache.txt"

#returns a set of all assignments currently on the calendar
def get_assignments():
	# get the links from the calendar page
	links_list = html_helper.get_calendar_links()
	assign_set = set() 
	#iterate through the links
	for link in links_list:
		#if the link is a lab of homework, add it to the set
		if "Lab" in link or "Homework" in link:
			assign = link.split(":")[0]
			if assign[-1] in "01234567890":
				assign_set.add(assign)
	return assign_set

#write a set of assignments to a file
def write_assignments(assign_set):
	f = open(assignment_file, 'w')
	f.write(repr(assign_set))
	f.close()

#returns a set of new assignments
def update_assignments():
	#read old assignments and get current assignments
	old_assigns = read_assignments()
	current_assigns = get_assignments()
	# return a tuple of the new assignment set and the current
	# assignment set
	return current_assigns - old_assigns, current_assigns


def read_assignments():
	try:
		return eval(open(assignment_file, 'r').read())
	except IOError:
		return set()

def should_countinue():
	try:
		open(escape_file)
		return False
	except IOError:
		return True


if __name__ == "__main__":
	write_assignments(get_assignments())