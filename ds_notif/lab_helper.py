import urllib

labURLBase = "http://www.cs.rpi.edu/academics/courses/%s/csci1200/labs/%s"

labURLSuffixes = ["",
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

numberOfLabs = len(labURLSuffixes) - 1

def getLabURL(semester, labNum):
	return labURLBase % (semester, labURLSuffixes[labNum])

def getLabName(semester, labNum):
	return "%s-%s.pdf" % (semester, labURLSuffixes[labNum].split("/")[-2])

def saveLab(semester, labNum):
	labURL = getLabURL(semester, labNum)
	f = open(getLabName(semester, labNum), 'wb') 
	f.write(urllib.urlopen(labURL).read())
	f.close()

if __name__ == "__main__":
	saveLab("fall15", 1)