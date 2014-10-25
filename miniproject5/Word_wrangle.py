"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    list2 = []
    for item in list1:
        if item not in list2:
            list2.append(item)
    return list2

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    if len(list1) < len(list2):
        return [item for item in list1 if item in list2]
    else:
        return [item for item in list2 if item in list1]

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in either list1 and list2.

    This function can be iterative.
    """   
    result = []
    while len(list1) >0 and len(list2) >0:
        if list1 [0] > list2 [0]:
            result.append(list2[0])
            list2 = list2[1:]
        else:
            result.append(list1[0])
            list1 = list1[1:]
    if len(list1) > 0:
        result += list1
    if len(list2) > 0:
        result += list2
    return result
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if len (list1) < 2:
        return list1
    else:
        mid = len (list1)/2
        left = merge_sort(list1[:mid])
        right = merge_sort(list1[mid:])
        return merge (left, right)

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    #print len(word)
    if len(word) < 1:
        #base case
        return [word]
    else:
        #recursive case
        first = word[0]
        rest = word[1:]
        new_string = []
        temp = gen_all_strings(rest)
        for item in temp:
            new_string += [item[:dummy_i] + first + item[dummy_i:] for dummy_i in range (len(item) + 1)]
        substring = temp + new_string
        return substring

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    output = []
    flie = urllib2.urlopen("http://codeskulptor-assets.commondatastorage.googleapis.com/assets_scrabble_words3.txt")
    for line in flie:
        #print line
        output.append(line[:-1])
    return output

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
codeskulptor.set_timeout(60)
run()


    
    
