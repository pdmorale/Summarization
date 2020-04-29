import sys
if not hasattr(sys, 'argv'):
    sys.argv= ['']
from langdetect import detect

def textToDgram(content,filePath,name,TranslateLang):
    TranslateE2J=False
    TranslateJ2E=False

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

#if __name__ == "__main__":
#    content1 = "President Trump repeatedly involved Vice President Pence in efforts to exert pressure on" \
#               " the leader of Ukraine at a time when the president was using other channels to solicit information" \
#               " that he hoped would be damaging to a Democratic rival, current and former U.S. officials said."
#    filePath1 = "C:\\Users\\pablo.morales\\Desktop\\Lenovo Back-up Win10\\Summarizer\\text_summary0717" \
#                "\\text_summary\\MyNewsGraph\\HTMLfiles"
#    name1 = "Whatever.html"

 #   print(textToDgram(content1,filePath1,name1,"English"))