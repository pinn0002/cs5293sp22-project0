import sqlite3
from project0 import project0
testurl = "https://www.normanok.gov/sites/default/files/documents/2022-03/2022-03-01_daily_incident_summary.pdf"
dbname = 'normanpd.db'
def test_fetchincidents():
    data = project0.fetchincidents(testurl)
    assert data is not None
def test_extractincidents():
    fetch = project0.fetchincidents(testurl)
    extractincidents = project0.extractincidents(fetch)
    assert isinstance(extractincidents,list)
def test_createdb():
    database = project0.createdb()
    assert database == dbname
def test_populatedb():
    db = project0.createdb()
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute('''SELECT * FROM incidents''')
    assert cur.fetchall() is not None
def test_status():
    db = project0.createdb()
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute('''SELECT nature,COUNT(nature) FROM incidents GROUP BY nature ORDER BY COUNT(nature) DESC, nature ASC''')
    assert cur.fetchall() is not None



