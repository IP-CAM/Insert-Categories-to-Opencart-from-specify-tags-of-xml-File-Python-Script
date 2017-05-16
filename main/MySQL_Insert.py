#Server Connection to MySQL:
import MySQLdb
import re
import time
#Vars of Opencart DB connect
dbHost = "localhost"
dbUser = "root"
dbPassword = "123456"
dbName = "dbname" 
dbCharset = 'utf8'
dbInit =  'SET NAMES UTF8' 
#Vars of Tables Opencart in process
#Tag name
tag = "span"
#Vars of IDs
rootId = 185 #Root ID ofr all categories
parentId = 186 #Current parent ID of adding subcategory
currentId = None #Current subcategory ID

conn = MySQLdb.connect(host= dbHost,
                  user=dbUser,
                  passwd=dbPassword,
                  db=dbName,
                  charset=dbCharset, 
                  init_command=dbInit)
x = conn.cursor()
conn.autocommit(True)

#Regex Rule
pattern = r"(?<=\<"+tag+"\>)(\s*.*\s*)(?=\<\/"+tag+"\>)"
#Regex for ru text from file
file = open("files/file-ru.txt", mode="r", encoding="utf-8")
fileString = file.read()
resultTextRu = re.findall(pattern, fileString)
#Regex for en text from file
file = open("files/file-en.txt", mode="r", encoding="utf-8")
fileString = file.read()
resultTextEn = re.findall(pattern, fileString)

if len(resultTextRu)==len(resultTextEn):
    print("lines Ru: "+  str(len(resultTextRu)) + "\nlines En: "+  str(len(resultTextEn)))
    print("Ok process! Go to next steps...")
else:
    print("Problem! Lines in En and Ru files are different...")
    raise SystemExit

outputText = ""
#Get max ID of subcategoryies, and increment it for last adding subcategory
x.execute("SELECT * FROM WebSofter_studilla.category ORDER BY category_id DESC LIMIT 0, 1")
data = x.fetchall()
for row in data :
    currentId = (int(row[0]) + 1)
    
try:
    for i in range(len(resultTextRu)):
        outputText +=resultTextRu[i] + "->" + resultTextEn[i] + "\n"
        #Add new subcategory
        x.execute("""INSERT INTO WebSofter_studilla.category VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (currentId, '', parentId, 0, 1, 0, 1, time.strftime('%Y-%m-%d %H:%M:%S'), time.strftime('%Y-%m-%d %H:%M:%S')))
        lastId = currentId
        #Add Rus lang for subcategory
        x.execute("""INSERT INTO WebSofter_studilla.category_description VALUES(%s, %s, %s, %s, %s, %s, %s)""",
        (lastId, 2, resultTextRu[i], "", resultTextRu[i], "", ""))
        #Add Eng lang for subcategory
        x.execute("""INSERT INTO WebSofter_studilla.category_description VALUES(%s, %s, %s, %s, %s, %s, %s)""",
        (lastId, 1, resultTextEn[i], "", resultTextEn[i], "", ""))
        #Path for level 0 in admin panel
        x.execute("""INSERT INTO WebSofter_studilla.category_path VALUES(%s, %s, %s)""",
        (lastId, rootId, 0))
        #Path for level 1 in admin panel
        x.execute("""INSERT INTO WebSofter_studilla.category_path VALUES(%s, %s, %s)""",
        (lastId, parentId, 1))
        #Path for level 2 in admin panel
        x.execute("""INSERT INTO WebSofter_studilla.category_path VALUES(%s, %s, %s)""",
        (lastId, lastId, 2))
        #Add Layout
        x.execute("""INSERT INTO WebSofter_studilla.category_to_layout VALUES(%s, %s, %s)""",
        (lastId, 0, 0))
        #Add in public side of site
        x.execute("""INSERT INTO WebSofter_studilla.category_to_store VALUES(%s, %s)""",
        (lastId, 0))
        print(lastId)
        #Increment added ID for next subcategory
        currentId += 1
    print(outputText)
    conn.commit()
except:
   conn.rollback()

conn.close()