import sqlite3
from project0 import project0
testurl = "https://www.normanok.gov/sites/default/files/documents/2022-03/2022-03-01_daily_incident_summary.pdf"
def test_extractincidents():
    fetch = project0.fetchincidents(testurl)
    extractincidents = project0.extractincidents(fetch)
    for item in extractincidents:
        assert len(item)==5
def test_status():
    db = project0.createdb()
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute('''DELETE FROM incidents''')
    assert cur.fetchall() == []
