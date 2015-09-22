# Description:

A Python module that finds the largest compound word in a 
file containing a newline-separated list of words.

Uses a dynamic programming approach to determine whether
a word of length K is a compound word in O(K^2) time,
and a Trie to avoid redundant storage of words' prefixes,
thereby improving memory usage. 

Given a list of N words, the algorithm therefore runs in
approximately O(NK^2), where K is the average length
of a word.

The Trie implementation allows the user to specify whether
they'd like to optimize for memory usage or speed by using
two different node implementations.

# Usage:

Running the program:
python find_compound.py filename