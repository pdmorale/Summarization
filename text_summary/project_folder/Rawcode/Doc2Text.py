import docx2txt
def doc2text(filePath):
    text = docx2txt.process(filePath).replace("\n","").replace("\u200b","")
    return text