# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 08:45:04 2020

@author: jclizaran
"""

#CHAPTER 11. REGULAR EXPRESSIONS

"""
Exercise 1: Write a simple program to simulate the operation of the
grep command on Unix. Ask the user to enter a regular expression and
count the number of lines that matched the regular expression:
"""

import re
reg_exp = input('Write a text: ')
count = 0
file_handler = open('mbox.txt')

for line in file_handler:
    if re.search(reg_exp,line):
        count += 1
print('num of lines where the text appear: ', count)

"""
Exercise 2: Write a program to look for lines of the form:
    New Revision: 39772
Extract the number from each of the lines using a regular expression
and the findall() method. Compute the average of the numbers and
print out the average as an integer.
"""

import re
fhand = open('mbox.txt')
count = 0
for line in fhand:
    if re.search('New Revision:',line):
        count += 1
print(count)


import re
fhand = open('mbox-short.txt')
count = 0
sum_nums = 0
list_total = list()
for line in fhand:
    if re.search('New Revision: ([0-9]+)',line):
        list_num = re.findall('New Revision: ([0-9]+)',line)
        #print(list_num)
        list_total.append(int(list_num[0]))
#print(list_total)

for num in list_total:
    count += 1
    sum_nums = sum_nums + num
average_value = sum_nums/count
print ('Average value: ',average_value)

"""
Exercise 1: Change the socket program socket1.py to prompt the user
for the URL so it can read any web page. You can use split('/') to
break the URL into its component parts so you can extract the host
name for the socket connect call. Add error checking using try and
except to handle the condition where the user enters an improperly
formatted or non-existent URL.
"""

import socket
import re
web_page = input ('Write a web page: ')
if len(web_page) < 1:
    web_page = 'http://data.pr4e.org/romeo.txt'
web_connect = re.match('http://([^/]+)',web_page).group(1)
print (web_connect)

mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


try:
    mysock.connect((web_connect, 80))
    cmd = ('GET http://'+ web_page + ' HTTP/1.0\r\n\r\n').encode()
    mysock.send(cmd)
except:
    print('Web name no valid')
    mysock.close()

while True:
    data = mysock.recv(512)
    if len(data) < 1:
        break
    print(data.decode(),end='')

mysock.close()

"""
Exercise 2: Change your socket program so that it counts the number
of characters it has received and stops displaying any text after it has
shown 3000 characters. The program should retrieve the entire document and count the total number of characters and display the count
of the number of characters at the end of the document.
"""

import socket
import re
web_page = input ('Write a web page: ')
if len(web_page) < 1:
    web_page = 'http://data.pr4e.org/romeo-full.txt'
web_connect = re.match('http://([^/]+)',web_page).group(1)
print ('connection: ', web_connect)

mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


try:
    mysock.connect((web_connect, 80))
    cmd = ('GET http://'+ web_page + ' HTTP/1.0\r\n\r\n').encode()
    mysock.send(cmd)
except:
    print('Web name no valid')
    mysock.close()

len_data = 0
text_total = ''
while True:
    data = mysock.recv(512)
    if len(data) < 1:
        break
    text_data = data.decode()
    len_data = len(text_data) + len_data
    text_total = text_total + text_data
    #print(text_data,end='')
    print(data)

print(text_total[0:3000])
print ('Longitud',len_data )
mysock.close()




"""
Exercise 3: Use urllib to replicate the previous exercise of (1) retrieving
the document from a URL, (2) displaying up to 3000 characters, and
(3) counting the overall number of characters in the document. Don’t
worry about the headers for this exercise, simply show the first 3000
characters of the document contents.
"""
import urllib.request
web_page = input ('Write a web page: ')
if len(web_page) < 1:
    web_page = 'http://data.pr4e.org/romeo-full.txt'
try:
    fhand = urllib.request.urlopen(web_page)
    print( 'Web_consulted:', web_page)
    text_total = ''
    for line in fhand:
        text_total = text_total + line.decode().strip() + '\n'
    
    print (text_total[0:2999])
    print ('Num_chars: ',len(text_total))
except:
    print('Web name no valid')

"""
Exercise 4: Change the urllinks.py program to extract and count paragraph (p) 
tags from the retrieved HTML document and display the
count of the paragraphs as the output of your program. Do not display
the paragraph text, only count them. Test your program on several
small web pages as well as some larger web pages.
"""

import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
url = input('Enter URL: ')
if len(url) < 1:
    url = 'http://data.pr4e.org/romeo-full.txt'
html = urllib.request.urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, 'html.parser')
# Retrieve all of the anchor tags

tags = soup('p')

#for tag in tags:
#    print('TAG: ',tag.string)
print('num_paragraphs:',len(tags))

#print(soup.title.string)

"""
Exercise 5: (Advanced) Change the socket program so that it only shows
data after the headers and a blank line have been received. Remember
that recv receives characters (newlines and all), not lines.
"""

import socket
import re
web_page = input ('Write a web page: ')
if len(web_page) < 1:
    web_page = 'http://data.pr4e.org/romeo-full.txt'
web_connect = re.match('http://([^/]+)',web_page).group(1)
print ('connection: ', web_connect)

mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


try:
    mysock.connect((web_connect, 80))
    cmd = ('GET http://'+ web_page + ' HTTP/1.0\r\n\r\n').encode()
    mysock.send(cmd)
except:
    print('Web name no valid')
    mysock.close()

len_data = 0
text_total = ''

End_header = False #  '\r\n'
while True:
    data = mysock.recv(512)
    if len(data) < 1:
        break
    text_data = data.decode()
    
    len_data = len(text_data) + len_data
    text_total = text_total + text_data
    #print(text_data,end='')
    #print(data)

#  print(text_total.find('\r\n\r\n')) ## busca la primera línea en blanco (doble salto de línea). Con ese índice se sabe cuando acaba la cabecera

print(text_total[(text_total.find('\r\n\r\n')+4):])
print ('Longitud',len_data )
mysock.close()

'''
Exercise 1: Change either geojson.py or geoxml.py to print out the two character country 
code from the retrieved data. Add error checking so
your program does not traceback if the country code is not there. Once
you have it working, search for “Atlantic Ocean” and make sure it can
handle locations that are not in any country.
'''


import urllib.request, urllib.parse, urllib.error
import json
import ssl
api_key = False
# If you have a Google Places API key, enter it here
# api_key = 'AIzaSy___IDByT70'
# https://developers.google.com/maps/documentation/geocoding/intro
if api_key is False:
    api_key = 42
    serviceurl = 'http://py4e-data.dr-chuck.net/json?'
else :
    serviceurl = 'https://maps.googleapis.com/maps/api/geocode/json?'
# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
while True:
    address = input('Enter location: ')
    if len(address) < 1: break
    parms = dict()
    parms['address'] = address
    if api_key is not False: parms['key'] = api_key
    url = serviceurl + urllib.parse.urlencode(parms)
    print('Retrieving', url)
    uh = urllib.request.urlopen(url, context=ctx)
    data = uh.read().decode()
    print('Retrieved', len(data), 'characters')
    try:
        js = json.loads(data)
    except:
        js = None
    if not js or 'status' not in js or js['status'] != 'OK':
        print('==== Failure To Retrieve ====')
        print(data)
        continue
    print(json.dumps(js, indent=4))
    lat = js['results'][0]['geometry']['location']['lat']
    lng = js['results'][0]['geometry']['location']['lng']
    print('lat', lat, 'lng', lng)
    if js['results'][0]['types'][0]=='country':
        print('Country code: ', js['results'][0]['address_components'][0]['short_name'])
    else:
        print('This is not a country: It is a', js['results'][0]['types'][0])
    location = js['results'][0]['formatted_address']
    print(location)