# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 17:32:13 2020

@author: jclizaran
"""

print("Hello World!!!!")

#CHAPTER 2: VARIABLES, EXPRESSIONS, AND STATEMENTS
#Exercise 2: Write a program that uses "input" to prompt a user for their name and then welcomes them.

name = input("Write your name: ")
print('Hi, '+ name)

#Exercise 3: Write a program to prompt the user for hours and rate perhour to compute gross pay.

hours = input("Enter hours worked: ")
rate  = input("Enter rate per hour: ")
print("salary received: ", int(hours) * int(rate), " euros")

#Exercise 4: Assume that we execute the following assignment statements:

width = 17
height = 12.0

width//2
width/2.0
height/3
1+2*5

#Exercise 5: Write a program which prompts the user for a Celsius temperature, convert the temperature to Fahrenheit, and print out the converted temperature.

temp_celsius = input('Celsius Temperature: ')
temp_fahrenheit = (float(temp_celsius) * 9/5) + 32
print('temp_Fahrenheit: ',temp_fahrenheit)

#CHAPTER 3.  CONDITIONAL EXECUTION

#Exercise 1: Rewrite your pay computation to give the employee 1.5 times the hourly rate for hours worked above 40 hours.
hours = float(input("Enter hours worked: "))
rate  = float(input("Enter rate per hour: "))

if hours <= 40:
    salary = hours * rate
else:
    salary = 40 * rate + (hours - 40) * rate * 1.5

print("salary received: ", salary, " euros")

#Exercise 2: Rewrite your pay program using try and except so that your program handles non-numeric input gracefully by printing a message and exiting the program. The following shows two executions of the program:
try:
    hours = float(input("Enter hours worked: "))
    rate  = float(input("Enter rate per hour: "))
except:
    hours = -1
    rate  = -1

if hours >= 0 and hours <= 40:
    salary = hours * rate
elif hours > 40:
    salary = 40 * rate + (hours - 40) * rate * 1.5
else:
    salary = 'Incorrect Input values'
print("salary received in euros: ", salary)

#Exercise 3: Write a program to prompt for a score between 0.0 and1.0. If the score is out of range, print an error message. If the score is between 0.0 and 1.0, print a grade using the following table:
try:
    result_num = float(input('Write the result of the exam in number, between 0 and 1: '))
    if result_num >= 0 and result_num <= 1:
        print('Resultado válido')
    else:
        print('Resultado no válido')
        result_num = -1
except:
    result_num = -1
    print('Dato de entrada incorrecto')
if result_num >= 0.9:
    print('A')
elif result_num >= 0.8:
    print('B')
elif result_num >= 0.7:
    print('C')
elif result_num >= 0.6:
    print('D')
elif result_num > -1:
    print('F')

#CHAPTER 4. FUNCTIONS

#Exercise 6: Rewrite your pay computation with time-and-a-half for overtime and create a function called computepay which takes two parameters(hours and rate).

try:
    hours = float(input("Enter hours worked: "))
except:
    hours = -1
try:
    rate  = float(input("Enter rate per hour: "))
except:
    rate  = -1

def computepay(hours,rate):
    if hours >= 0 and hours <= 40:
        salary = hours * rate
    elif hours > 40:
        salary = 40 * rate + (hours - 40) * rate * 1.5
    else:
        salary = -1
    return salary
if hours < 0:
    print('Hours value incorrect')
elif rate < 0:
    print('rate value incorrect')
else:
    salary = computepay(hours,rate)

if salary < 0:
    print('Datos entrada incorrectos')
else:
    print('salary received in euros: ', salary)

#Exercise 7: Rewrite the grade program from the previous chapter usinga function called computegrade that takes a score as its parameter and returns a grade as a string.

def result_letra(result_num):
    if result_num >= 0.9:
        result_letra ='A'
    elif result_num >= 0.8:
        result_letra ='B'
    elif result_num >= 0.7:
        result_letra ='C'
    elif result_num >= 0.6:
        result_letra ='D'
    else:
        result_letra ='F'
    return result_letra
  
try:
    result_num = float(input('Write the result of the exam in number, between 0 and 1: '))
    if result_num >= 0 and result_num <= 1.0:
        print('Resultado válido')
        result_w = result_letra(result_num)
    else:
        print('Resultado no válido')
        result_num = -1
except:
    result_num = -1


if result_num < 0:
    print('Dato de entrada incorrecto')
else:
    print('Test result: ',result_w)

"""
Exercise 1: Write a program which repeatedly reads numbers until the
user enters “done”. Once “done” is entered, print out the total, count,
and average of the numbers. If the user enters anything other than a
number, detect their mistake using try and except and print an error
message and skip to the next number.
"""

total_nums = 0
count_nums = 0
average_nums = 0
input_data = None
while count_nums < 20 and input_data != 'done':
    try:
        input_data = input('Write a number(write "done" then Enter to exit: ')
        input_num = float(input_data)
    except:
        if input_data != 'done':
            print('No introdujo un número válido')
        continue
    total_nums = total_nums + input_num
    count_nums = count_nums + 1
    average_nums = total_nums/count_nums
    print('Total: ',total_nums)
    print('Count: ',count_nums)
    print('Average: ',average_nums)
print('End Program')

#CHAPTER 5. ITERATION

"""
Exercise 2: Write another program that prompts for a list of numbers
as above and at the end prints out both the maximum and minimum of
the numbers instead of the average.
"""

total_nums = 0
count_nums = 0
max_nums = None
min_nums = None
input_data = None
while count_nums < 20 and input_data != 'done':
    try:
        input_data = input('Write a number(write "done" then Enter to exit: ')
        input_num = float(input_data)
    except:
        if input_data != 'done':
            print('No introdujo un número válido')
        continue
    if max_nums == None:
        max_nums = input_num
    if min_nums == None:
        min_nums = input_num
    total_nums = total_nums + input_num
    count_nums = count_nums + 1
    if input_num > max_nums:
        max_nums = input_num
    if input_num < min_nums:
        min_nums = input_num

    print('Total: ',total_nums)
    print('Count: ',count_nums)
    print('Max Num: ',max_nums)
    print('Min Num: ',min_nums)
print('End Program')