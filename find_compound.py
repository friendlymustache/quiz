'''
A python module that finds the largest compound word in a 
list of words.
'''
import sys

class Node:
	def __init__(self, key, first_child=None):
		self.first_child = first_child
		self.key = key
		self.next = None
		self.isWord = False

	def get(self, char):		
		current = self.first_child
		while current is not None and current.key != char:
			current = current.next
		return current			

class Trie:
	def __init__(self):
		self.root = Node(None)

	def insert(self, word):
		current = self.root
		for char in word:
			# Look up each character in the word, moving down the Trie
			# as we go.
			# If the current character is present, then continue 
			# to move down the Trie - otherwise, insert a node.
			first_child = current.first_child
			next = current.get(char)
			if next is None:
				next = Node(char)
				next.next = current.first_child
				current.first_child = next				
			current = next
		current.isWord = True			
			
	def lookup(self, word):
		current = self.root
		for char in word:
			current = current.get(char)
			if current is None:
				return False
		return current.isWord				

	def isWordCompound(self, word):
		n = len(word)
		# opt[i] is True if the suffix of <word>
		# starting with its ith character is 
		# 1) a compound word or 
		# 2) a word in the list (except for i = 0)		
		opt = [False] * (n + 1)
		# The empty string is a valid "word"
		# in the dictionary
		opt[n] = True
		for i in range(n - 1, -1, -1):
			current = self.root		
			end = i + min(n - i, n - 1)	
			for j in range(i, end):
				# Walk along the trie using the jth character
				# of the current word
				current = current.get(word[j])
				# If current prefix is invalid, stop
				if current is None:
					break
				# If the suffix of our current substring
				# is in our dictionary, our current substring
				# is a compound word, so note this and break
				elif current.isWord and opt[j + 1]:
					opt[i] = True
					break			
		return opt[0]				

def longestCompoundWord(trie, words):
	max_length = 0
	solution = ""
	for word in words:
		if trie.isWordCompound(word) and len(word) > max_length:
			max_length = len(word)
			solution = word
	return solution



if __name__ == "__main__":

	if len(sys.argv) != 2:
		print "Usage: python find_compound.py <filename>"
	else:		
		filename = sys.argv[1]

		trie = Trie()
		words = []
		f = open(filename)
		for line in f:
			line = line.strip()
			trie.insert(line)
			words.append(line)

		print longestCompoundWord(trie, words)	
