
'''
    Read from files, print and count category items in specify tags
'''
import re
tagName = "span"

fileRu = open("files/file-ru.html", mode="r", encoding="utf-8")
fileStringRu = fileRu.read()
fileEn = open("files/file-en.html", mode="r", encoding="utf-8")
fileStringEn = fileEn.read()

pattern = r"(?<=\<span\>)(\s*.*\s*)(?=\<\/span\>)"
resultTextRu = re.findall(pattern, fileStringRu)
resultTextEn = re.findall(pattern, fileStringEn)

outputText = ""
i = 0
for itemRu in resultTextRu:
    outputText +=itemRu + "->"+ resultTextEn[i] +"\n"
print(outputText)

if len(resultTextRu)==len(resultTextEn):
    print("lines Ru: "+  str(len(resultTextRu)) + "\nlines En: "+  str(len(resultTextEn)))
    print("Ok process! Got to next steps...")
else:
    print("Problem! Lines in En and Ru files are different...")
    raise SystemExit
