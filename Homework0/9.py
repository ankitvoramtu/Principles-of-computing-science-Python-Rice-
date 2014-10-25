# -*- coding: utf-8 -*-
"""
Created on Mon Jun  9 21:29:19 2014

@author: zhihuixie
"""
import poc_simpletest
def appendsum(lst):
    for i in range(25):
        lst.append(sum(lst[len(lst)-3:]))
    return lst
sum_three = [0, 1, 2]
a = appendsum(sum_three)
print a[20]

