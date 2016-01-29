import urllib

lab_url_base = "http://www.cs.rpi.edu/academics/courses/%s/csci1200/labs/%s"

lab_url_suffixes = [
		"01_getting_started/lab_post.pdf",
		"02_classes/lab_post.pdf",
		"03_pointers/lab_post.pdf",
		"04_debugging/lab_post.pdf",
		"05_vectors/lab_post.pdf",
		"06_lists_iterators/lab_post.pdf",
		"07_list_implementation/lab_post.pdf",
		"08_recursion/lab_post.pdf",
		"09_maps/lab_post.pdf",
		"10_sets/lab_post.pdf",
		"11_operators/lab_post.pdf",
		"12_hash_tables/lab_post.pdf",
		"13_order_notation/lab_post.pdf",
		"14_smart_memory/lab_post.pdf"
]

number_of_labs = len(lab_url_suffixes)

def get_lab_url(semester, lab_no):
	return lab_url_base % (semester, lab_url_suffixes[lab_no])

def get_lab_name(semester, lab_no):
	return "%s-%s.pdf" % (semester, lab_url_suffixes[lab_no].split("/")[-2])

def save_lab(semester, lab_no):
	lab_url = get_lab_url(semester, lab_no)
	f = open(get_lab_name(semester, lab_no), 'wb') 
	f.write(urllib.urlopen(lab_url).read())
	f.close()

if __name__ == "__main__":
	save_lab("fall15", 1)