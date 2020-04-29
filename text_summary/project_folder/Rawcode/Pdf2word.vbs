Set oWord = CreateObject("Word.Application")
Dim FilePath
Dim DocmPath
Set args = WScript.Arguments
FilePath = args.Item(0)
DocmPath = args.Item(1)

' Like args_parse() of python
' ***** Debug **********
' "C:\Users\pablo.morales\Desktop\PDF2Word2.docm"
oWord.Visible = False
oWord.Documents.Open DocmPath, ,False
oWord.Run "DisablePDFWarning", CStr(FilePath)
oWord.Quit