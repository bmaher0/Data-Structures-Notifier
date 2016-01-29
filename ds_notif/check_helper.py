import lab_helper, pdf_helper
from pdfminer.pdfparser import PDFSyntaxError

current_semester = "spring16"

def download_lab_pdfs():
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
		print "Good PDF!"
		return date[2:6] == "2016"
	except PDFSyntaxError:
		print "Bad PDF!"
		return None

if __name__ == "__main__":
	download_lab_pdfs()
	print check_mod_dates()
