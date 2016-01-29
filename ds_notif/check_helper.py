import lab_helper, pdf_helper
from pdfminer.pdfparser import PDFSyntaxError

current_semester = "spring16"
escape_file = "stop.txt"

def refresh():
	for i in range(lab_helper.number_of_labs):
		lab_helper.save_lab(current_semester, i)

def check_mod_dates():
	output = []
	for i in range(lab_helper.number_of_labs):
		filename = lab_helper.get_lab_name(current_semester, i)
		output.append(check_mod_date(filename))
	return output

def check_mod_date(filename):
	try:
		date = pdf_helper.get_pdf_mod_date(filename)
		return date[2:6] == "2016"
	except PDFSyntaxError:
		return None

def check(current_max):
	refresh()
	new_max = check_mod_dates().index(True)
	if new_max > current_max:
		print "New lab! Lab #%d has been posted!" % (new_max+1)
		return new_max
	return current_max

def should_countinue():
	try:
		open(escape_file)
		return False
	except IOError:
		return True

def cleanup():
	#TODO nake function to remove pdfs after main ends
	pass

if __name__ == "__main__":
	pass
