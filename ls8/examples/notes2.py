#bitwise stuff I guess

'''
AND, OR, NOT, XOR

Operation        Boolean Operator        Bitwise Operator
AND (if a and b)   &&                      &
OR  (if a or b)    ||                      |
NOT (if a not b)    !                      ~
XOR (None :/   )    None :/                ^


AND
  0b1010101
& 0b1000101 (and these together)
--------------
0b1001101

#so when they 
are both 1, you put down a 1
anything else is a 0

  0b0011100
& 0b1010101
------------
    0010100

OR

  0b1010101
| 0b1000101
------------
  0b1010101

#if either number is a 1, we write down a 1
#need two 0s to output false

  0b0011100
| 0b1010101
------------
  0b1011101

NOT

~0b001110
---------
 0b110001

#return the opposite

XOR

True xor False --> True
True xor True --> False
False xor False --> False

#true if exactly one statement is true
#only one true can return true

  0b1010101
^ 0b1000101
---------
0b0010000

  0b0011100
^ 0b1010101
---------
0b1001001


Shifting
essentially delete the last howver many numbers
if shifting to the right

0b1010101 >> 1
--------------
0b101010

0b1010101 >> 2
-------------
0b10101

0b1010101 >> 3
--------------
0b1010

on the left shift, you shove it over and add zeros to the end

0b1010101 << 1
-----------
0b10101010

0b1010101 << 2
----------
0b101010100

How to isolate bits we are interested in?
we can shift it to chop off all the other bits, and focus on certain bits

if you want numbers all the way to the right, right shift
if we have two numbers in the middle, we can right shift and then we do masking

Masking :

we create the mask to isolate the bits that we want

if we want the last 10:

    1010
&   0011 <-- mask
---------
0010

see we blocked out the first two numbers with the 0
and have the opprotunity to get a number with a 1


say we want just the last two nums

  10101
& 00011 <-- mask
--------
  00001

  those first zeros are meaningless, so now we only have the number we want


if we put in all 1s, then we will get a copy of the original values


This has to do with our homework, we want just the first two numbers
The first two bits show the number of times we need to increment the program counter
tells you how many arguments that the method takes

ADD
10100000

10100000 >> 6:
10


this will allow us to not have to write the pc count every time
pc += 1 + (command >> 6)

'''

#this will help us finish todays project
#how to read a file in? (to load in different commands)
import sys

# #does not auto close file
# file = open("print8.ls8", 'r')
# lines = file.read()
# print(lines)

if len(sys.argv) < 2:
    print('Please pass in a second file name.')

    sys.exit()
#[0] is the name of the file we are going to run
#[1] is the name of the one we want to load
try:
    file_name = sys.argv[1]
    #auto closes file
    with open(file_name) as file:
        for line in file:
            # this makes it so we can just get the commands in the file
            split_line = line.split('#')
            command = split_line[0].strip()

            if command == '':
              continue 
            
            #convert from string to int
            num = int(command, 2)
          

            print(f'{num:b} is {num}')
except FileNotFoundError:
    print(f'{sys.argv[1]} file was not found.')