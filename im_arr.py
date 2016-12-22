#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# coding=utf-8
"""
Created on Wed Dec 21 02:01:56 2016

@author: alexzerphy

This program compares different compression methods and 
compresses data using a run-length algorithm.

process:
    reads the bytes from the file and determines if any redundance exists
    in the neighboring bytes.  Then it determines how many times the byte 
    appears in succession and stores that value which will be used later for 
    decompression
    
example:
    if my file had the byte composition:
        \xff\xff\xd8\x00\xda\x00\x00\xd8
    
    the compressed file will read:
        \xff\xd8\x00\xda\x00\xd8
    and the factor array will read:
        [2, 1, 1, 1, 2, 1]
"""

import zlib, sys
import numpy as np


#image before compression
with open('Apple1.jpg', 'rb') as f: #open file in read mode
    data = f.read() #read the byte data of the file and store it in data
    
print(data[:51]) #print the first 50 elements of data



print('\n') #newline
#image after compression
comp = zlib.compress(data, 9) #compress the data using the zlib algorithm
print(comp[:51]) #print the first 50 elements of the compressed data


#size comparison
print('Raw size:  ', sys.getsizeof(data)) #print size of the data
print('Comp size:  ', sys.getsizeof(comp)) #print size of the compressed data



#Compression algorithm test
'''print(data[0:5]) #lines used for debugging
print(data[2])'''
factor = 1 #redundance factor (how many times the same byte appears in consecutive order)
factarr = np.zeros(len(data)) #initialize the array of factors with zeros
compstr = b"" #create empty byte string
for i in data: #for each byte in data...
    if data[i] == data[i+1]: #if 2 consecutive elements are the same...
        factor += 1 #increment the factor
    else:
        factor = 1 #otherwise set the factor to 1
        
    if data[i] != data[i-1]: #if the current element is not equal to the previous element...
        compstr += data[i:i+1] #append the byte slice to the byte string
    
    factarr[i] = factor #append the factor to the factor array
'''print(compstr[0:5]) #lines used for debugging
print(factarr[0:1])'''

print('Compstr Size:  ', sys.getsizeof(compstr)) #print size of compressed data
print('Factarr Size:  ', sys.getsizeof(factarr)) #print size of factor array



a = [b'' for i in compstr] #initialize array with len(compstr) number of empty byte strings
tempstring = b'' #temporary byte string used to make code cleaner
string = b'' #empty byte string to combine elements of array into a single string
for i in compstr: #for every byte in compstr...
    if factarr[i] > 1: #if a factor is greater than 1...
        a[i : i + int(factarr[i]) - 1] = compstr[i:i+1] #set array slice (depends on factor) to compstr slice
    else:
        a[i:i+1] = compstr[i:i+1] #otherwise set the single array slice equal to the single compstr 

for i in range(0,len(a)): #for integer from 0 to len(a)...
    tempstring = a[i] #set temporary string equal to array byte
    string += bytes(tempstring) #append to final string

#for i in range(0, len(a)):
 #   b[i:i+1] = a[i:i+1]
#print (string[0:51])
#print(bytes(a[0:1])) #line used for debugging
print('String size:  ', sys.getsizeof(string)) #print size of string
#print (a[0:51])