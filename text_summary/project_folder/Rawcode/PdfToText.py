import fitz

def pdfToText(filePath):
    doc = fitz.open(filePath)
    text = ""
    for i in range(doc.pageCount):
        text += doc.loadPage(i).getText("text").replace("\n","")
    return text
