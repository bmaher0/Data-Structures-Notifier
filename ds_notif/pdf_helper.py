from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument

def get_pdf_mod_date(filename):
	fp = open(filename, 'rb')
	parser = PDFParser(fp)
	doc = PDFDocument(parser)
	return doc.info[0]["ModDate"]

if __name__ == "__main__":
	print get_pdf_first_line("spring16-01_getting_started.pdf")