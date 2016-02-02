import html_helper

escape_file = "stop.txt"
filename = "assignments_cache.txt"

def get_assignments():
	links_list = html_helper.get_calendar_links()
	assign_set = set() 
	for link in links_list:
		if "Lab" in link or "Homework" in link:
			assign = link.split(":")[0]
			if assign[-1] in "01234567890":
				assign_set.add(assign)
	return assign_set

def write_assignments(assign_set):
	f = open(filename, 'w')
	for assign in assign_set:
		f.write(assign + '\n')

#returns a set of new assignments
def new_assignments():
	old_assigns = read_assignments()
	current_assigns = get_assignments()
	return current_assigns - old_assigns, current_assigns

def read_assignments():
	assign_set = set()
	try:
		for assign in open(filename, 'r'):
			assign_set.add(assign.strip())
	except IOError:
		pass
	return assign_set

def should_countinue():
	try:
		open(escape_file)
		return False
	except IOError:
		return True


if __name__ == "__main__":
	write_assignments(get_assignments())