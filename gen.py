#!/usr/local/bin/python

import os, re, sqlite3
from bs4 import BeautifulSoup, NavigableString, Tag

db = sqlite3.connect('./docSet.dsidx')
cur = db.cursor()

try:
    cur.execute('DROP TABLE searchIndex;')
except:
    pass

cur.execute('CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT);')
cur.execute('CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path);')

docpath = './Documents'

def gen_index(filename):
    page = open(os.path.join(docpath,filename)).read()
    soup = BeautifulSoup(page)

    body_div = soup.find('div', {'class': 'body'})
    for section_div in body_div.find_all('div', {'class': 'section'}, recursive=False):
        for dl in section_div.find_all('dl', recursive=False):
            try:
                name = dl.dt.attrs["id"]
                path = filename + dl.dt.a.attrs["href"]
                cur.execute('INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)', (name, 'Directive', path))
            except:
                continue

gen_index("index.html")

db.commit()
db.close()
