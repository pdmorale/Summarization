import docx2txt
import fitz
import text_summary
import Graphmaker

def doc2text(filePath):
    text = docx2txt.process(filePath).replace("\u200b","")
    return text

def pdfToText(filePath):
    doc = fitz.open(filePath)
    text = ""
    for i in range(doc.pageCount):
        text += doc.loadPage(i).getText("text").replace("\n", " ").replace(".", ".\n")
    return text

def extract_text(filePath):
    if filePath.endswith(".pdf"):
        text = pdfToText(filePath)
    elif filePath.endswith(".docx") or filePath.endswith(".doc"):
        text = doc2text(filePath)
    else:
        try:
            raise ValueError("Incorrect file type: file must be either pdf or word document.")
        except ValueError as e:
            print(e)
    return text

def document_summarizer(filePath, ratio, word):
    raw_text = extract_text(filePath)
    summarized_text = text_summary.Summarizer(raw_text, ratio, word)
    return summarized_text

def document_to_graph(DocfilePath, SaveFilePath, name, GoogleT):
    raw_text = extract_text(DocfilePath)
    path = Graphmaker.textToDgram(raw_text,SaveFilePath,name,TranslateLang=GoogleT)
    return path

# DocfilePath = "C:/Users/yuki.tachibana/Downloads/test.docx"
# SaveFilePath = "Output/HTMLfiles/"
# name = "Temp.html"
# GoogleT=""
# document_to_graph(DocfilePath, SaveFilePath, name, GoogleT)