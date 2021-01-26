# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 19:43:56 2020

@author: jclizaran
"""

#CHAPTER 6. STRINGS
"""
Exercise 5: Take the following Python code that stores a string:
str = 'X-DSPAM-Confidence:0.8475'
Use find and string slicing to extract the portion of the string after the
colon character and then use the float function to convert the extracted
string into a floating point number.
"""

str = 'X-DSPAM-Confidence:0.8475'
output_E5 = float(str[str.find(':')+1:])

"""
Exercise 6: Read the documentation of the string methods at
https://docs.python.org/library/stdtypes.html#string-methods You
might want to experiment with some of them to make sure you
understand how they work. strip and replace are particularly useful.
The documentation uses a syntax that might be confusing. For example,
in find(sub[, start[, end]]), the brackets indicate optional arguments.
So sub is required, but start is optional, and if you include start, then
end is optional.
"""
#str = 'X-DSPAM-Confidence:0.8475'
#str_replaced_1 = str.replace(')
#
#dir

#CHAPTER 7. FILES
"""
Exercise 1: Write a program to read through a file and print the contents
of the file (line by line) all in upper case. Executing the program will
look as follows:
"""
file_name = input('Enter file name: ')
try:
    fhand = open('mbox-short.txt')
except:
    print('File can not be opened',file_name)
    exit()
count = 0
for line in fhand:
    count += 1
    print(count,line.upper())
    
"""
Exercise 2: Write a program to prompt for a file name, and then read
through the file and look for lines of the form:
    X-DSPAM-Confidence: 0.8475
When you encounter a line that starts with “X-DSPAM-Confidence:”
pull apart the line to extract the floating-point number on the line.
Count these lines and then compute the total of the spam confidence
values from these lines. When you reach the end of the file, print out
the average spam confidence.
"""
#   mbox-short.txt

file_name = input('Enter file name: ')
try:
    fhand = open(file_name)
    count = 0
    count_spam = 0
    total_spam_confidence = 0
    for line in fhand:
        count += 1
        if line.startswith('X-DSPAM-Confidence:'):
            count_spam += 1
            print(count,line.upper())
            total_spam_confidence = total_spam_confidence + float(line[20:26])
    print('Spam average confidence: ',total_spam_confidence/count_spam)
except:
    print('File can not be opened',file_name)
    exit()


"""
Exercise 3: Sometimes when programmers get bored or want to have a
bit of fun, they add a harmless Easter Egg to their program. Modify
the program that prompts the user for the file name so that it prints a
funny message when the user types in the exact file name “na na boo
boo”. The program should behave normally for all other files which
exist and don’t exist. Here is a sample execution of the program:
"""

file_name = input('Enter file name: ')  
try:
    if file_name.upper() == 'NA NA BOO BOO':
        print("NA NA BOO BOO TO YOU - You have been punk'd!")

    else: 
        fhand = open(file_name)
        count = 0
        count_spam = 0
        total_spam_confidence = 0
        for line in fhand:
            count += 1
            if line.startswith('X-DSPAM-Confidence:'):
                count_spam += 1
                print(count,line.upper())
                total_spam_confidence = total_spam_confidence + float(line[20:26])
        print('Spam average confidence: ',total_spam_confidence/count_spam)
except:
    print('File can not be opened',file_name) 
    exit()

#CHAPTER 8. LISTS

"""
Exercise 1: Write a function called chop that takes a list and modifies
it, removing the first and last elements, and returns None. Then write
a function called middle that takes a list and returns a new list that
contains all but the first and last elements.
"""


def c8_chop(list_e1=list()):
    del list_e1[0]
    del list_e1[-1]
    
def c8_middle(list_e1=list()):
    del list_e1[0]
    del list_e1[-1] 
    return list_e1
try_c8_chop = list()
try_c8_chop = ['red','yellow','blue','black','white']
print(try_c8_chop)
output_middle = c8_middle (try_c8_chop)

c8_chop(try_c8_chop)
print(try_c8_chop)

"""
Exercise 2: Figure out which line of the above program is still not
properly guarded. See if you can construct a text file which causes the
program to fail and then modify the program so that the line is properly
guarded and test it to make sure it handles your new text file.
"""
"""
Exercise 3: Rewrite the guardian code in the above example without
two if statements. Instead, use a compound logical expression using
the or logical operator with a single if statement.
"""
# Code:
"""
fhand = open('mbox-short.txt')
count = 0
for line in fhand:
words = line.split()
# print('Debug:', words)
if len(words) == 0 : continue
if words[0] != 'From' : continue
print(words[2])
"""
# What if? line hasn't 3 words ---> error
fhand = open('mbox-short.txt')
count = 0
for line in fhand:
    words = line.split()
    # print('Debug:', words)
    if len(words) == 0 or words[0] != 'From' : continue
    try:
        print(words[2])
    except:
        print('There is not 3 words in this lane')


"""
Exercise 4: Download a copy of the file www.py4e.com/code3/romeo.txt.
Write a program to open the file romeo.txt and read it line by line. For
each line, split the line into a list of words using the split function.
For each word, check to see if the word is already in a list. If the word
is not in the list, add it to the list. When the program completes, sort
and print the resulting words in alphabetical order.
"""
fhand = open('romeo.txt')
word_list = list()
for line in fhand:
    words = line.split()
    for word in words:
        if word not in word_list:
            word_list.append(word.lower())
word_list.sort()
print(word_list)
"""
Exercise 5: Write a program to read through the mail box data and
when you find line that starts with “From”, you will split the line into
words using the split function. We are interested in who sent the
message, which is the second word on the From line.
You will parse the From line and print out the second word for each
From line, then you will also count the number of From (not From:)
lines and print out a count at the end. This is a good sample output
with a few lines removed:
"""
fhand = open('mbox-short.txt')
count=0
word_list_e5 = list()
for line in fhand:
    words = line.split()
    if len(words) == 0 or words[0] != 'From' : continue
    count = count+1
    word_list_e5.append(words[1])
print(count)
print(word_list_e5)
"""
Exercise 6: Rewrite the program that prompts the user for a list of
numbers and prints out the maximum and minimum of the numbers at
the end when the user enters “done”. Write the program to store the
numbers the user enters in a list and use the max() and min() functions to
compute the maximum and minimum numbers after the loop completes.
"""

num_list_e6 = list()
input_data = ''
count=0
while input_data != 'done':
    
    input_data = input('Write a number: ')
    if input_data == 'done': continue
    try:
        num_list_e6.append(float(input_data))
        count += 1
    except:
        print('Not a valid number')
        continue
print('max_number: ',max(num_list_e6))
print('min_number: ',min(num_list_e6))
print('Thanks for using this program')      

#CHAPTER 9. DICTIONARIES

"""
Exercise 1: Download a copy of the file www.py4e.com/code3/words.txt
Write a program that reads the words in words.txt and stores them as
keys in a dictionary. It doesn’t matter what the values are. Then you
can use the in operator as a fast way to check whether a string is in the
dictionary.
"""

fhand = open('words.txt')
dict_ej1 = dict()
indice = 0
for line in fhand:
    words = line.split()
    for word in words:
        indice += 1
        dict_ej1[word]=indice
print(dict_ej1)

"""
if 'aressss' in dict_ej1:
    print ('We got it in the dictionary')
else:
    print('No, we did not have it')
"""

"""
Exercise 2: Write a program that categorizes each mail message by
which day of the week the commit was done. To do this look for lines
that start with “From”, then look for the third word and keep a running
count of each of the days of the week. At the end of the program print
out the contents of your dictionary (order does not matter).
"""

fhand = open('mbox-short.txt')
dict_ej2 = dict()
for line in fhand:
    words = line.split()
    if len(words) < 3 or words[0] != 'From' : continue
    if words[2] in dict_ej2:
        dict_ej2[words[2]] += 1
    else:
        dict_ej2[words[2]] = 1
print(dict_ej2)


"""
Exercise 3: Write a program to read through a mail log, build a histogram using
a dictionary to count how many messages have come from each email address, and
print the dictionary.
"""

fhand = open('mbox-short.txt')
dict_ej3 = dict()
for line in fhand:
    words = line.split()
    if len(words) < 2 or words[0] != 'From' : continue
    if words[1] in dict_ej3:
        dict_ej3[words[1]] += 1
    else:
        dict_ej3[words[1]] = 1
print(dict_ej3)


"""
Exercise 4: Add code to the above program to figure out who has the
most messages in the file. After all the data has been read and the 
dictionary has been created, look through the dictionary using a maximum
loop (see Chapter 5: Maximum and minimum loops) to find who has
the most messages and print how many messages the person has.
"""

fhand = open('mbox-short.txt')
dict_ej3 = dict()
for line in fhand:
    words = line.split()
    if len(words) < 2 or words[0] != 'From' : continue
    if words[1] in dict_ej3:
        dict_ej3[words[1]] += 1
    else:
        dict_ej3[words[1]] = 1
print(dict_ej3)

max_value = None
min_value = None

for key_word in dict_ej3:
    if max_value is None or (dict_ej3[key_word] > max_value):
        max_value = dict_ej3[key_word]
        max_value_index = key_word
    if min_value is None or (dict_ej3[key_word] < min_value):
        min_value = dict_ej3[key_word]
        min_value_index = key_word
print('Mininum value: ',min_value, 'dict Index: ',min_value_index)
print('Maximum value: ',max_value, 'dict Index: ',max_value_index)


"""
Exercise 5: This program records the domain name (instead of the
address) where the message was sent from instead of who the mail came
from (i.e., the whole email address). At the end of the program, print
out the contents of your dictionary.
"""

fhand = open('mbox-short.txt')
dict_ej5 = dict()
for line in fhand:
    words = line.split()
    if len(words) < 2 or words[0] != 'From' : continue
    email_address = words[1].split(sep='@')
    
    if len(email_address) < 2:continue
    if email_address[1] in dict_ej5:
        dict_ej5[email_address[1]] += 1
    else:
        dict_ej5[email_address[1]] = 1
print(dict_ej5)


""" Same implementation using function get() to reduce lines of code """

fhand = open('mbox-short.txt')
dict_ej5 = dict()
for line in fhand:
    words = line.split()
    if len(words) < 2 or words[0] != 'From' : continue
    email_address = words[1].split(sep='@')
    
    if len(email_address) < 2:continue
    dict_ej5[email_address[1]] = dict_ej5.get(email_address[1],0) + 1
    
print(dict_ej5)


#CHAPTER 10. TUPLES

"""
Exercise 1: Revise a previous program as follows: Read and parse the
“From” lines and pull out the addresses from the line. Count the number of messages from each person using a dictionary.
After all the data has been read, print the person with the most commits
by creating a list of (count, email) tuples from the dictionary. Then
sort the list in reverse order and print out the person who has the most
commits.
"""

fhand = open ('mbox-short.txt')
dict_ej101 = dict()
for line in fhand:
    words = line.split()
    if len(words) < 2 or words[0] != 'From': continue
    dict_ej101[words[1]] = dict_ej101.get(words[1],0) + 1

list_ej101 = list()
for k,v in dict_ej101.items():
    list_ej101.append([v,k])
    
    
print(dict_ej101)
print(list_ej101)
list_ej101.sort(reverse=True)
print(list_ej101)

print('Person who has the most commits: ', list_ej101[1][1], '// Num. commits: ', list_ej101[1][0])


"""
Exercise 2: This program counts the distribution of the hour of the day
for each of the messages. You can pull the hour from the “From” line
by finding the time string and then splitting that string into parts using
the colon character. Once you have accumulated the counts for each
hour, print out the counts, one per line, sorted by hour as shown below.
"""


fhand = open ('mbox-short.txt')
dict_ej102 = dict()
hour = list()
for line in fhand:
    words = line.split()
    if len(words) < 6 or words[0] != 'From': continue
    hour = words[5].split(sep=':')
    dict_ej102[hour[0]] = dict_ej102.get(hour[0],0) + 1
list_ej102 = list()
for h,num in dict_ej102.items():
    list_ej102.append([h,num])
list_ej102.sort()
for x in list_ej102:
    print(x)


"""
Exercise 3: Write a program that reads a file and prints the letters
in decreasing order of frequency. Your program should convert all the
input to lower case and only count the letters a-z. Your program should
not count spaces, digits, punctuation, or anything other than the letters
a-z. Find text samples from several different languages and see how
letter frequency varies between languages. Compare your results with
the tables at https://wikipedia.org/wiki/Letter_frequencies.
"""

import string
fhand = open ('mbox-short.txt')
alphabet = string.ascii_lowercase
dict_ej3 = dict()
list_letters = list()
total_num_letters = 0
for line in fhand:
    for letter in line:
        if letter.lower() in alphabet:
            dict_ej3[letter.lower()] = dict_ej3.get(letter.lower(),0) + 1
for data in dict_ej3:
    total_num_letters = total_num_letters + dict_ej3[data]
print(dict_ej3)
for x in dict_ej3:
    dict_ej3[x] = dict_ej3[x] / total_num_letters
print(dict_ej3)
for x,y in dict_ej3.items():
    list_letters.append([y,x])
list_letters.sort(reverse=True)
for letter in list_letters:
    print(letter)
