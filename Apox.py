#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 12:48:47 2016

@author: Alexander J. Zerphy

purpose:
    Reads data byte-by-byte from a file and "compresses" it by creating a 
    unique "blueprint" of the file.  Then, using the blueprint, the file can 
    be rebuilt byte-by-byte exactly the way it was before with no data 
    loss or corruption.
input:
    Reads data from file
processing:
    Uses 'with' keyword to open the file and read data without having to
    manually close the file at the end of the program.  The bytes are 
    read as an array of int values and converted to an array of byte values 
    by reindexing the array with values of the array slices, i.e. data[i] 
    becomes data[i:i+1].  As the bytes are read, they are stored as keys 
    in a dictionary with an array type value.  The array holds the indexes 
    where those bytes appear in the file.  To decompress the file, the length 
    of the file is found by determining the largest index stored in the 
    dictionary and an array is initialized with length + 1 empty byte strings.
    For-loops then replace these empty byte strings with the bytes from the 
    dictionary by placing them at the indexes stored in the array.  Then each 
    element of the resulting array are joined into a single continuous byte 
    string.  This is the same series of bytes that was read from the data 
    at the beginning.  Finally the size is printed to determine that no 
    data has been deleted.
output:
    A dictionary that tell the program how to build the file. /
    A string of bytes that make up the file
"""
import time, sys, numpy as np


class Apox:
    def __init__(self, path, data, comp):
        """Initialize all class variables"""
        self.path = path #path of the file to compress
        self.data = data #empty array
        self.comp = comp #empty dictionary
    
    def read_data(self):
        """Read data from file byte-by-byte"""
        with open(self.path, 'rb') as f: #open the file for read only (in bytes) and automatically close file when finished
            self.data = f.read()
        return self.data
    
    def compress(self):
        """Compress data"""
        temp = {} #temporary dictionary that holds the key-value pair for a single iteration of the for-loop
        i = 0
        for num in self.data:
            byte = self.data[i:i+1]
            if byte not in self.comp: #if the byte has not been counted, add it to the dictionary
                temp = {byte: [i]}
            else:
                self.comp[byte].append(i) #if the byte has been counted, append the index of the byte to the value of the corresponding key in the dictionary
            i += 1
            self.comp.update(temp) #adds the temporary entry to the compression dictionary
        return self.comp
        
    def decompress(self):
        temp = [] #temporary array to store the results of a single for-loop
        decomp = [] #array of decompressed data
        for key in self.comp:
            temp.append(max(self.comp[key])) #append the maximum value found in the dictionary
        length = max(temp) #the maximum of these values is the length
        decomp = [b'' for i in range(0,length + 1)] #initialize decompression data to an array of empty byte strings
        
        """
        This is where the problem is:
            These loops iterate through each index stored in each key and
            places the key into each of the indices of the decomp array.
            
        for example:
            self.comp = {b'\x00': [0,3,4], b'\xff': [1,5], b'\xda': [2]}
                         After the loops the decompressed data will look like:
                             decomp = [b'\x00', b'\xff', b'\xda', b'\x00', b'\x00', b'\xff']
        
                             
                             
        The code works.  However it takes a very long time to complete with 
        files larger than a few MB whereas the compression algorithm 
        finishes almost instantly.  Is there a way to improve efficiency?
        """
        ##################################
        for key in self.comp:
            for index in self.comp[key]:
                decomp[index] = key
        ##################################

        decompstr = b'' 
        i = 0
        for index in decomp:
            decompstr += decomp[i] #combines all elements of decomp into a single byte string
            i += 1
        return decompstr
    
a = Apox('../Apple1.jpg',[],{}) 
a.read_data()
compressed = a.compress()
decompressed = a.decompress()


'''
#ORIGINAL CODE

def read_data(path):
    """Read data from file byte-by-byte."""
    with open(path, 'rb') as f:
        data = f.read()
    return data

def compress(data):
    """Compress data."""
    d = {}
    temp = {}
    i = 0
    for num in data:
        byte = data[i:i+1]
        if byte not in d:
            temp = {byte: [i]}
        else:
            d[byte].append(i)
        i += 1
        d.update(temp)
    return d


def decompress(comp):
    """Decompress data."""
    temp = []
    decomp = []
    for key in comp:
        temp.append(max(comp[key]))
    length = max(temp)
    decomp = [b'' for i in range(0, length + 1)]
    
    for key in comp:
        for index in comp[key]:
            decomp[index] = key
    decompstr = b''
    i = 0
    for index in decomp:
        decompstr += decomp[i]
        i += 1
    return decompstr


def size(d):
    """Return size of d."""
    s = sys.getsizeof(d)
    unit = ''
    if s >= 1024:
        s /= 1024 #bytes to kilobytes
        unit = 'KB'
    if s >= 1024*1024:
        s /= (1024*1024)
        unit = 'MB'
    return (str(s) + ' ' + unit)
    
start = time.time()
#path = 'Apple1.jpg'
#path = 'hack.jpg'
#path = 'Apple_32bit_raw_09/
#path = '750KB.jpg'
#path = 'test.txt'
path = 'lesms10.txt'
data = read_data(path)
data = data[0:2000000]
print (data)
comp = compress(data)
print (comp)
decomp = decompress(comp)
print (decomp)
end = time.time()

t = end - start
print('took ' + str(t) + ' seconds')

print('Size of compressed data:  ' + size(comp))
print('Size of the data is ' + size(data))
print('Size of decompressed data: ' + size(decomp))'''