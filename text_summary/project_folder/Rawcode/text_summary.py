from langdetect import detect
import sys
import codecs
if not hasattr(sys, 'argv'):
    sys.argv= ['']

ratio = 0.2
word = "Disabled"
def Summarizer (text, ratio, word):
	language = detect(text)
	if word == "Disabled":
		if language == "en":
			from summa.summarizer import summarize
			smzTxt = summarize(text, ratio=float(ratio))
		else:
			from textrank.summa import summarizer
			smzTxt = summarizer.summarize(text, ratio=float(ratio))
	else:
		if language == "en":
			from summa.summarizer import summarize
			smzTxt = summarize(text, words=int(word))
		else:
			from textrank.summa import summarizer
			smzTxt = summarizer.summarize(text, words=int(word))

	outputText = ",".join(smzTxt).replace(",", "")
	with codecs.open("temp.txt", 'w', 'utf-8', 'ignore') as f:
		f.write(outputText)
	# f = open("temp.txt", "w").close()
	# 	f = open("temp.txt", "w+")
	return outputText

