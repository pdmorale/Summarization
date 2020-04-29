import sys
if not hasattr(sys, 'argv'):
    sys.argv= ['']
from langdetect import detect

def textToDgram(content,filePath,name,TranslateLang):
    import text_summary
    content = text_summary.Summarizer(content,ratio=0.3,word=200)
    TranslateE2J=False
    TranslateJ2E=False
    content = content.encode(encoding='CP932', errors='ignore').decode(encoding='shift_jis',errors='ignore')
    if TranslateLang == "English":
        TranslateJ2E = True
    if TranslateLang == "Japanese":
        TranslateE2J = True

    language = detect(content)
    if language == "en":
        import MyNewsGraphEN
        Miner = MyNewsGraphEN.NewsMining(content,filePath,name,TranslateE2J=TranslateE2J)
    else:
        import MyNewsGraphJP
        Miner = MyNewsGraphJP.NewsMining(content,filePath,name,TranslateJ2E=TranslateJ2E)
    if Miner == None:
        return ""
    else:
        Miner.saveHTML()
    return Miner.fullPath

# import codecs
# with codecs.open("bug.txt", 'r', 'utf-8', 'ignore') as f:
#     rawtext = f.read()
#
# SaveFilePath = "Output/HTMLfiles/"
# name = "Temp.html"
# GoogleT=""
# textToDgram(rawtext,SaveFilePath,"Temp.html",GoogleT)

# import codecs
# with codecs.open("bug.txt", 'r', 'utf-8', 'ignore') as f:
#     rawtext = f.read()
# from textrank.summa import keywords
# print(keywords.keywords(rawtext))
# print(keywords.keywords(rawtext, language="japanese"))
