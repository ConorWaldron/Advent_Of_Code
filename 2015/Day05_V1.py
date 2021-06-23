#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advent of Code 2015 Day 5
"""
import time
import numpy as np
start_time = time.time() #starts timer

#Import list of strings
with open ("Day5_input.txt", "r") as myfile:
    Input_Strings = myfile.readlines()

Nice = [] #create list of nice strings
Naughty = [] # create list of naughty strings

Number_Failed1 = 0 # Initilise counter to count number of strings that failed condition 1
Number_Failed2 = len(Input_Strings) # Initilise counter to count number of strings that failed condition 2
Number_Failed3 = 0 # Initilise counter to count number of strings that failed condition 3
 
for String_Entry in Input_Strings:
    
    #condition 1, check if at least 3 vowels are present
    Vowels = ['a', 'e', 'i', 'o', 'u']  
    Vowel_counter = np.zeros(len(Vowels)) # array that records number of that vowels
    i = 0 # reset counter
    for specific_vowel in Vowels:
        Vowel_counter[i] =  String_Entry.count(specific_vowel) #count number of times that vowel was mentioned
        i += 1 # move counter on to next vowel
    Number_Vowels = np.sum(Vowel_counter)
    if Number_Vowels > 2:
        condition1 = True
    else:
        condition1 = False
        Number_Failed1 += 1 #count the number of failed strings for condition 1
 
    #condition 2 check if it contains at least 1 letter that appears twice in a row
    #I can either do 'aa' in String_Entry, looped for all 26 letters in alphabet
    #Or I can split string into their 17 characters and check if each character is the same as the next one, looped for all 17
    #I choose to loop over len of string as its shorter than number of letters in alophabet
    condition2 = False
    for j in range(0, len(String_Entry)-1):  #dont go to final entry as there is no letter after final to compare to
        if String_Entry[j] == String_Entry[j+1]:
            condition2 = True
            Number_Failed2 -= 1 # counts the number that failed condition2, by counting how many passed it and subtraction
            break #We dont want to continue checking strings for two sets of replicates
    
    #condition 3 check if the string does not contain the strings ab, cd, pq, or xy
    condition3 = False # swap to true if it contains a banned string
    banned = ['ab', 'cd', 'pq', 'xy']  #list of banned strings
    for banned_combo in banned:
        if banned_combo in String_Entry:
            condition3 = True    
            Number_Failed3 += 1 #count the number that fail number 3
            break # stop checking for duplicate number of banned entries
    
    #logic to combine three requirments
    if ((condition1 and condition2) and (condition3==False)):  # requires 1 and 2 to be true, and 3 to be false
        Nice.append(String_Entry)
    else:
        Naughty.append(String_Entry)

Number_Nice = len(Nice)
Number_Naughty = len(Naughty)
print('The number of nice strings is {}'.format(Number_Nice))
print('The number of naughty strings is {}'.format(Number_Naughty))

end_time = time.time()
duration = end_time - start_time
print('The code took {} milliseconds to execute'.format(1000*duration))
