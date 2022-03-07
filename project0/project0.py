import re
import urllib.request
import tempfile
import PyPDF2
import sqlite3
import pandas as pd
def fetchincidents(url):
    headers = {}
    headers['user-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
    data = urllib.request.urlopen(urllib.request.Request(url, headers=headers)).read()
    return data
def extractincidents(incident_data):
    fp = tempfile.TemporaryFile()
    #write the pdf data to a temp file
    fp.write(incident_data)
    fp.seek(0)
    pdfReader = PyPDF2.pdf.PdfFileReader(fp)
    #count the total pages in pdf
    pagecount = pdfReader.getNumPages()
    #extract all text from 1st page of pdf file
    page = pdfReader.getPage(0).extractText()
    #remove title in the first page and handle multiline text in page1
    page = page.replace('NORMAN POLICE DEPARTMENT\n','').replace('Daily Incident Summary (Public)\n','').replace(' \n', '')
    #extract text from all the remaining pages and handle multiline text and to combine all pdf pages together
    for pagenum in range(1,pagecount):
        page += pdfReader.getPage(pagenum).extractText().replace(' \n', '')
    #remove extra space at the end of file
    page = page.rstrip('\n')
    #split the data at each occurence of date and time
    page = re.split(r'\s+(?=\d{1,2}/\d{1,2}/\d{4} \d{1,2}:\d{1,2})', page)
    pagelist = []
    #skip the column header row in range
    for i in range(1, len(page)):
        l = page[i].split('\n')
        # replace null values with NA and append to pagelist
        if len(l) == 3:
            l.extend(["NA","NA"])
            l[2], l[4] = l[4], l[2]
            pagelist.append(l)
        #append to the pagelist only if 5 parameters available
        elif len(l) == 5:
            pagelist.append(l)
    return pagelist
def createdb():
    #connect to the database normanpd.db
    con = sqlite3.connect('normanpd.db')
    #for executing SQL commands
    cur = con.cursor()
    #drop table if already available
    cur.execute('''DROP TABLE IF EXISTS incidents''')
    #create a table incidents
    cur.execute('''CREATE TABLE IF NOT EXISTS incidents(incident_time TEXT,incident_number TEXT,incident_location TEXT,nature TEXT,incident_ori TEXT)''')
    #save changes to the database
    con.commit()
    #close the database
    con.close()
    return 'normanpd.db'
def populatedb(db,incidents):
    #connect to the database normanpd.db
    con = sqlite3.connect('normanpd.db')
    #for executing SQL commands
    cur = con.cursor()
    #insert all data to database
    cur.executemany('INSERT INTO incidents VALUES (?,?,?,?,?)',incidents)
    #save changes to database
    con.commit()
    #close database
    con.close()
def status(db):
    #connect to database normanpd.db
    con = sqlite3.connect('normanpd.db')
    #use pandas to read seql query
    df = pd.read_sql_query('''SELECT nature,COUNT(nature) FROM incidents GROUP BY nature ORDER BY COUNT(nature) DESC, nature ASC''',con)
    #join nature and COUNT(nature) columns with '|'
    df = df['nature'].map(str)+ '|' +df['COUNT(nature)'].map(str)
    #remove the index column
    print(df.to_string(index=False))
    con.commit()
    con.close()

