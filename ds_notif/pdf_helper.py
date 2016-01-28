from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument

def getPDFModDate(filename):
	fp = open(filename, 'rb')
	parser = PDFParser(fp)
	doc = PDFDocument(parser)
	return doc.info[0]["ModDate"]

if __name__ == "__main__":
	print modDateIn2016(getPDFModDate("spring16-01_getting_started.pdf"))
	print modDateIn2016(getPDFModDate("fall15-01_getting_started.pdf"))