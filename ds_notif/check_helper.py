import lab_helper, pdf_helper
from pdfminer.pdfparser import PDFSyntaxError

current_semester = "spring16"
number_of_labs = 14

def downloadLabPDFs():
	for i in range(1, number_of_labs + 1):
		lab_helper.saveLab(current_semester, i)

def printModDates():
	for i in range(1, number_of_labs + 1):
		filename = lab_helper.getLabName(current_semester, i)
		print checkModDate(filename)

def checkModDate(filename):
	try:
		date = pdf_helper.getPDFModDate(filename)
		print "Good PDF!",
		return date[2:6] == "2016"
	except PDFSyntaxError:
		print "Bad PDF!",
		return False
	

if __name__ == "__main__":
	downloadLabPDFs()
	printModDates()
