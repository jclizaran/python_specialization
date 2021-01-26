# -*- coding: utf-8 -*-
"""
Created on Sun Nov  8 15:54:30 2020

@author: jclizaran
"""
'''Example 1: Counting Email in a Database'''
import pyodbc

conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-DHVN9RG;"
        "Database=py4e;"
        "Trusted_Connection=yes;"
        )

cursor = conn.cursor()
#cursor.execute('DROP TABLE Counts')
cursor.execute('DROP TABLE IF EXISTS Counts') #DROP TABLE IF EXISTS table_name - works from version sql server 2016
cursor.execute('CREATE TABLE Counts (email NVARCHAR(256), count INTEGER)')

fname = input('Enter file name: ')
if (len(fname) < 1): fname = 'mbox-short.txt'
fh = open(fname)

for line in fh:
    if not line.startswith('From: '): continue
    pieces = line.split()
    email = pieces[1]
    cursor.execute('SELECT count FROM Counts WHERE email = ? ',(email,))
    row = cursor.fetchone()
    if row is None:
        cursor.execute('''INSERT INTO Counts (email, count)
        VALUES(?, 1)''', (email,))
    else:
        cursor.execute('UPDATE Counts SET count = count + 1 WHERE email = ?',(email,))
    conn.commit()

sqlstr = 'SELECT top 20 email, count FROM Counts ORDER BY count DESC'

for row in cursor.execute(sqlstr):
    print(str(row[0]), row[1])

conn.close()
#data = cursor.fetchall()


#cursor.execute("INSERT INTO First_table (name,email) VALUES ('Pepito Grillo','pepegrillo@grillo.com')")

#Example 2: twspider.py

from urllib.request import urlopen
import urllib.error
import twurl
import json
import pyodbc
import ssl


TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-DHVN9RG;"
        "Database=py4e;"
        "Trusted_Connection=yes;"
        )
cursor = conn.cursor()
cursor.execute ('''
IF NOT EXISTS (SELECT * FROM py4e.information_schema.tables where table_name = 'twitter')
begin
	CREATE TABLE  py4e.dbo.twitter (name NVARCHAR(1000), retrieved INTEGER, friends INTEGER)
end ''')
# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

while True:
    acct = input('Enter a Twitter account, or quit: ')
    if (acct == 'quit'): break
    if (len(acct) < 1):
        cursor.execute('SELECT top 1 name FROM py4e.dbo.twitter WHERE retrieved = 0')
        try:
            acct = cursor.fetchone()[0]
        except:
            print('No unretrieved Twitter accounts found')
            continue
    url = twurl.augment(TWITTER_URL, {'screen_name': acct, 'count': '10000'})
    print ('Retrieving', url)
    connection = urlopen(url, context = ctx)
    data = connection.read().decode()
    headers = dict(connection.getheaders())
    
    print('Remaining', headers['x-rate-limit-remaining'])
    js = json.loads(data)
    #Debugging
    # print json.dumps(js, indent=5)
    
    cursor.execute ('UPDATE py4e.dbo.twitter SET retrieved=1 WHERE name = ?', (acct, ))
    
    countnew = 0
    countold = 0
    for u in js['users']:
        friend = u['screen_name']
        print(friend)
        cursor.execute('SELECT top 1 friends FROM py4e.dbo.twitter WHERE name = ?', (friend, ))
        try:
            count = cursor.fetchone()[0]
            cursor.execute('UPDATE py4e.dbo.twitter SET friends = ? WHERE name = ?', (count+1, friend))
            countold = countold + 1
        except:
            cursor.execute('''INSERT INTO py4e.dbo.twitter (name, retrieved, friends) VALUES (?, 0, 1)''',(friend, ))
            countnew = countnew + 1
    print('New accounts=', countnew, ' revisited=', countold)
    conn.commit()
cursor.close()
        
#Example 3: Tracks.py

import xml.etree.ElementTree as ET
import pyodbc

conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-DHVN9RG;"
        "Database=py4e;"
        "Trusted_Connection=yes;"
        )
cursor = conn.cursor()

#NOTA: El uso de los distintos tipos de comillas para la construcción de las consultas SQL, permite insertar los elementos de la lista en la consulta
#Delete tables if they exists previously
table_list = ['Artist','Album','Track']
for table in table_list:
    sql001 = "IF EXISTS (SELECT * FROM py4e.information_schema.tables where table_name = '"+ table +"')" +'\n' +'BEGIN '+'\n'+"DROP TABLE " + table + "\n" +'END'
    print(sql001)            
    cursor.execute(sql001)
#Create new tables
sql002 = "CREATE TABLE py4e.dbo.Artist (id INTEGER NOT NULL PRIMARY KEY IDENTITY(1,1), name NVARCHAR(256) UNIQUE)"
print (sql002)
cursor.execute(sql002)
sql002 = "CREATE TABLE py4e.dbo.Album (id INTEGER NOT NULL PRIMARY KEY IDENTITY(1,1), artist_id INTEGER, title NVARCHAR(256) UNIQUE)"
print (sql002)
cursor.execute(sql002)
sql002 = "CREATE TABLE py4e.dbo.Track (id INTEGER NOT NULL PRIMARY KEY IDENTITY(1,1), album_id INTEGER, title NVARCHAR(256) UNIQUE, len INTEGER, rating INTEGER, count INTEGER)"
print (sql002)
cursor.execute(sql002)

fname = input('Enter file name: ')
if (len(fname) < 1) : fname = 'Library.xml'

# Function define to check the file 
def lookup(d, key):
    found = False
    for child in d: 
        if found : return child.text
        if child.tag == 'key' and child.text == key :
            found = True
    return None

stuff = ET.parse(fname)
all = stuff.findall('dict/dict/dict')
print ('Dict count: ', len(all))
for entry in all:
    if ( lookup(entry, 'Track ID') is None ) : continue
    
    name = lookup(entry, "Name")
    name = name.replace("/","\/")
    name = name.replace("'","\'")
    name = "War Pigs/Luke's Wall"
    
    
    artist = lookup(entry, 'Artist')
    album = lookup(entry, 'Album')
    count = lookup(entry, 'Play Count')
    rating = lookup(entry, 'Rating')
    length = lookup(entry, 'Total Time')
    
    if name is None or artist is None or album is None:
        continue
    print(name, artist, album, count, rating, length)
    
    sql0031 = "IF NOT EXISTS (SELECT * FROM py4e.dbo.Artist where name = '"+ artist +"')" +'\n' +'BEGIN '+'\n'+"INSERT INTO py4e.dbo.Artist(name) VALUES ( '" + artist + "' )" + "\n" +'END'
    print(sql0031)
    cursor.execute (sql0031)
    sql0032 = "SELECT id FROM py4e.dbo.Artist WHERE name = '"+ artist +"' "
    print(sql0032)
    cursor.execute (sql0032)
    artist_id = cursor.fetchone()[0]
    
    sql0041 = "IF NOT EXISTS (SELECT * FROM py4e.dbo.Album where title = '"+ album +"')" +'\n' +'BEGIN '+'\n'+"INSERT INTO py4e.dbo.album(title,artist_id) VALUES ( '" + album + "','" + str(artist_id) + "' )" + "\n" +'END'
    print(sql0041)
    cursor.execute (sql0041)
    sql0042 = "SELECT id FROM py4e.dbo.Album WHERE title = '"+ album +"' "
    print(sql0042)
    cursor.execute (sql0042)
    album_id = cursor.fetchone()[0]

    sql0051 = "IF NOT EXISTS (SELECT * FROM py4e.dbo.Track where title = '"+ name +"')" +'\n' +'BEGIN '+'\n'+"INSERT INTO py4e.dbo.Track(title,album_id,len,rating,count) VALUES ( '" + name + "'," + str(album_id) + "," + str(length) + "," + str(rating) + "," + str(count) + " )" + "\n" +'END'
    print(sql0051)
    cursor.execute (sql0051)
    
    conn.commit()

cursor.close()

#Example 3: roster.py

import json
import pyodbc

conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-DHVN9RG;"
        "Database=py4e;"
        "Trusted_Connection=yes;"
        )

cursor = conn.cursor()


#Delete tables if they exists previously
table_list = ['tUser','Member','Course']
for table in table_list:
    sql001 = "IF EXISTS (SELECT * FROM py4e.information_schema.tables where table_name = '"+ table +"')" +'\n' +'BEGIN '+'\n'+"DROP TABLE " + table + "\n" +'END'
    print(sql001)            
    cursor.execute(sql001)

#Create new tables
sql002 = "CREATE TABLE py4e.dbo.tUser (id INTEGER NOT NULL PRIMARY KEY IDENTITY(1,1), name NVARCHAR(256) UNIQUE)"
print (sql002)
cursor.execute(sql002)
sql002 = "CREATE TABLE py4e.dbo.Course (id INTEGER NOT NULL PRIMARY KEY IDENTITY(1,1), title NVARCHAR(256) UNIQUE)"
print (sql002)
cursor.execute(sql002)
sql002 = "CREATE TABLE py4e.dbo.Member (user_id INTEGER, course_id INTEGER, role INTEGER, PRIMARY KEY (user_id,course_id))"
print (sql002)
cursor.execute(sql002)

fname = input ('Enter file name: ')
if len(fname) < 1:
    fname = 'roster_data_sample.json'

str_data = open(fname).read()
json_data = json.loads(str_data)

for entry in json_data:
    name = entry[0]
    title = entry[1]
    role = entry[2]
    
    print(name,title)
    
    sql0031 = "IF NOT EXISTS (SELECT * FROM py4e.dbo.tUser where name = '"+ name +"')" +'\n' +'BEGIN '+'\n'+"INSERT INTO py4e.dbo.tUser(name) VALUES ( '" + name + "' )" + "\n" +'END'
    print(sql0031)
    cursor.execute (sql0031)
    sql0032 = "SELECT id FROM py4e.dbo.tUser WHERE name = '"+ name +"' "
    print(sql0032)
    cursor.execute (sql0032)
    user_id = cursor.fetchone()[0]

    sql0041 = "IF NOT EXISTS (SELECT * FROM py4e.dbo.Course where title = '"+ title +"')" +'\n' +'BEGIN '+'\n'+"INSERT INTO py4e.dbo.Course(title) VALUES ( '" + title + "' )" + "\n" +'END'
    print(sql0041)
    cursor.execute (sql0041)
    sql0042 = "SELECT id FROM py4e.dbo.Course WHERE title = '"+ title +"' "
    print(sql0042)
    cursor.execute (sql0042)
    course_id = cursor.fetchone()[0]

    sql0051 = "IF NOT EXISTS (SELECT * FROM py4e.dbo.Member where user_id = '"+ str(user_id) +"' AND course_id = '"+ str(course_id) +"')" +'\n' +'BEGIN '+'\n'+"INSERT INTO py4e.dbo.Member(user_id,course_id) VALUES ( '" + str(user_id) + "', '" + str(course_id) + "' )" + "\n" +'END'
    print(sql0051)
    cursor.execute (sql0051)


conn.commit()
cursor.close()


# Example 4: Twfriends.py

import urllib.request, urllib.parse, urllib.error
import twurl
import json
import ssl

TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

import pyodbc

conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-DHVN9RG;"
        "Database=py4e;"
        "Trusted_Connection=yes;"
        )
cursor = conn.cursor()

cursor.execute ('''
IF NOT EXISTS (SELECT * FROM py4e.information_schema.tables where table_name = 'people')
begin
	CREATE TABLE  py4e.dbo.people (id INTEGER NOT NULL PRIMARY KEY IDENTITY(1,1), name NVARCHAR(1000) UNIQUE, retrieved INTEGER)
end ''')

cursor.execute ('''
IF NOT EXISTS (SELECT * FROM py4e.information_schema.tables where table_name = 'follows')
begin
	CREATE TABLE  py4e.dbo.follows (from_id INTEGER, to_id INTEGER, UNIQUE(from_id,to_id))
end ''')


ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

while True:
    acct = input('Enter a Twitter account, or quit: ')
    if (acct == 'quit'): break
    if (len(acct)<1):
        cursor.execute('SELECT top 1 id, name FROM People WHERE retrieved = 0')
        try:
            (id, acct) = cursor.fetchone()
        except:
            print('No unretrieved Twitter accounts found')
            continue
    else:
        sql401 = "SELECT top 1 id FROM People WHERE name = '" + str(acct) + "'"
        cursor.execute(sql401)
        try:
            id = cursor.fetchone()[0]
        except:
            sql402 = "IF NOT EXISTS (SELECT * FROM py4e.dbo.people where name = '"+ str(id) +"' AND retrieved = 0 )" +'\n' +'BEGIN '+'\n'+"INSERT INTO py4e.dbo.people(name,retrieved) VALUES ( '" + str(acct) + "', 0 )" + "\n" +'END'
            cursor.execute(sql402)
            #cur.execute('''INSERT OR IGNORE INTO People (name, retrieved) VALUES (?, 0)''',(acct, ))

            conn.commit()
            if cursor.rowcount != 1:
                print('Error inserting account:',acct)
                continue
            #id = cursor.fetchval()
            id = cursor.execute("SELECT id FROM py4e.dbo.people where name = '"+ str(id) +"'" ).fetchone()[0]
    url = twurl.augment(TWITTER_URL, {'screen_name':acct, 'count':'100'})
    print('Retrieving account',acct)
    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()
    headers = dict(connection.getheaders())
    
    print('Remaining', headers['x-rate-limit-remaining'])
    
    try:
        js = json.loads(data)
    except:
        print('Unable to parse json')
        print(data)
        break
    
    #Debugging
    #print(json.dumps(js, indent=4))
    
    if 'users' not in js:
        print('Incorrect JSON received')
        print(json.dumps(js,indent=4))
        continue
    
    sql403 = "UPDATE People SET retrieved=1 WHERE name = '" + acct +"'"
    cursor.execute (sql403)
    #### !!! REVISAR ESTA QUERY. name is UNIQUE
    #cursor.execute('UPDATE People SET retrieved=1 WHERE name = ? LIMIT 1', (friend, ))
    countnew = 0
    countold = 0
    for u in js['users']:
        friend = u['screen_name']
        print(friend)
        cursor.execute("SELECT TOP 1 id FROM py4e.dbo.people WHERE name = '" + friend + "'")
        try:
            friend_id = cursor.fetchone()[0]
            countold = countold + 1
        except:
            sql404 = "IF NOT EXISTS (SELECT * FROM py4e.dbo.people where name = '"+ str(friend) +"' AND retrieved = 0 )" +'\n' +'BEGIN '+'\n'+"INSERT INTO py4e.dbo.people(name,retrieved) VALUES ( '" + str(friend) + "', 0 )" + "\n" +'END'
            cursor.execute(sql404)
            #cur.execute('''INSERT OR IGNORE INTO People (name, retrieved) VALUES (?, 0)''', (friend, ))
            conn.commit()
            if cursor.rowcount != 1:
                print('Error inserting account:', friend)
                continue
            #friend_id = cursor.fetchval()
            friend_id = cursor.execute("SELECT id FROM py4e.dbo.people where name = '"+ str(friend) +"'" ).fetchone()[0]
            countnew = countnew + 1
        sql405 = "IF NOT EXISTS (SELECT * FROM py4e.dbo.follows where from_id = '"+ str(id) +"' AND to_id = '"+ str(friend_id) +"' )" +'\n' +'BEGIN '+'\n'+"INSERT INTO py4e.dbo.follows (from_id,to_id) VALUES ( '" + str(id) + "', '" + str(friend_id) + "' )" + "\n" +'END'
        cursor.execute(sql405)
    #cur.execute('''INSERT OR IGNORE INTO Follows (from_id, to_id) VALUES (?,?)''', (id, friend_id))
    print('New accounts=', countnew, ' revisited=', countold)
    conn.commit()


