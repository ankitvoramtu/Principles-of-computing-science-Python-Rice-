# -*- coding: utf-8 -*-
"""
Created on Mon Jun  9 21:29:19 2014

@author: zhihuixie
"""

def merge(line):
    newline = [0]*len(line)
    count_of_num_in_newline = 0
    temp_store = [num for num in line if num != 0]
    for i in range (len(temp_store) - 1):  #merge adjacent number if they are equal
        if temp_store[i] == temp_store[i + 1]:
            temp_store[i] = 2*temp_store[i]
            temp_store[i + 1] = 0
    for number in temp_store:  #move number to newline
        if number != 0:
            newline[count_of_num_in_newline] = number
            count_of_num_in_newline += 1
    return newline
print merge([2, 4, 3, 3])

