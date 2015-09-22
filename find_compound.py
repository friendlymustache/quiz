'''
A Python module that finds the largest compound word in a 
list of words.
'''
import sys
import time

# The size of the alphabet our list of words is built from.
# Currently, we assume that all of our words consist only
# of lowercase letters, but this can be changed to support
# alphanumeric strings etc.
ALPHABET_SIZE = 26

class MemNode:
	'''
	A memory-efficient trie node implementation.
	Stores its children in a linked-list to minimize
	memory usage.
	'''
	def __init__(self, key):
		'''
		Create a new node with the specified key (character).
		'''		
		self.key = key
		# A reference to the next child node of the
		# current node's parent.
		self.next = None
		# A boolean indicating whether or not the current
		# Trie node represents the final character of a word.
		self.isWord = False
		# A reference to the head of the node's linked-list
		# of children
		self.first_child = None

	def get_child(self, char):	
		'''
		Returns the child of the current node corresponding
		to the passed-in character, or None if no such
		child exists.
		'''
		current = self.first_child
		while current is not None and current.key != char:
			current = current.next
		return current		

	def addChild(self, char):
		'''
		Adds a child node corresponding to the passed-in
		character to the current node. Returns the newly-created
		child node.
		'''
		# Create a new child node
		child = MemNode(char)
		# Insert the new child node at the head of our
		# current node's linked list of children
		child.next = self.first_child
		self.first_child = child
		return child

class Node:
	'''
	A standard trie node implementation that uses
	an array to store its child nodes.
	'''
	def __init__(self, key):
		'''
		Create a new node with the specified key (character).
		'''				
		self.key = key
		# We store children as an array of the same size
		# as our alphabet - self.children[i] contains
		# the child representing the ith character in our
		# alphabet, or None if no such child exists.
		self.children = [None] * ALPHABET_SIZE
		self.isWord = False

	def get_child(self, char):	
		'''
		Returns the child of the current node corresponding
		to the passed-in character, or None if no such
		child exists.
		'''		
		return self.children[ord(char) - ord('a')]

	def addChild(self, char):	
		'''
		Adds a child node corresponding to the passed-in
		character to the current node. Returns the newly-created
		child node.
		'''		
		child = Node(char)
		self.children[ord(char) - ord('a')] = child
		return child


class Trie:
	def __init__(self, optimize_memory=False):
		'''
		Initializes a new Trie. Specify optimize_memory=True
		to use a more memory-efficient node representation
		in the Trie.
		'''
		self.optimize_memory = optimize_memory
		if optimize_memory:
			self.root = MemNode(None)
		else:
			self.root = Node(None)

	def insert(self, word):
		'''
		Insert a word into the Trie, creating new nodes
		where necessary
		'''
		current = self.root
		for char in word:
			# Look up each character in the word, moving down the Trie
			# as we go.
			# If the current character is present, then continue 
			# to move down the Trie - otherwise, insert a node.
			next = current.get_child(char)
			if next is None:
				next = current.addChild(char)		
			current = next
		# Set the isWord flag to once we've reached the node
		# representing the final character of our word, 
		current.isWord = True			
			
	def lookup(self, word):
		'''
		Returns True if a word is present in the Trie and False otherwise.
		'''
		current = self.root
		for char in word:
			current = current.get_child(char)
			if current is None:
				return False
		return current.isWord				

	def isWordCompound(self, word):
		'''
		Returns True if the passed-in word is compound
		(can be formed by concatenating words in the Trie)
		and False otherwise.
		'''
		n = len(word)
		# opt[i] is True if the suffix of <word>
		# starting with word[i] is:
		# 1) a compound word or 
		# 2) a word in the list (except for i = 0)		
		opt = [False] * (n + 1)
		# The empty string is a valid "word"
		# in the dictionary
		opt[n] = True
		# Iterate through all valid staerting indices
		# for a suffix of <word>, starting with n - 1
		for i in range(n - 1, -1, -1):
			current = self.root					
			end = i + min(n - i, n - 1)	
			# Iterate through all prefixes of our current
			# suffix and look them up in the trie. If
			# the prefix is present in our trie and the
			# remaining portion of the suffix is a compound
			# word, the entire suffix is a compound word.
			# Note that for the suffix consisting
			# of all of the characters in <word> (i = 0),
			# we exclude the prefix consisting of the
			# entire suffix.
			for j in range(i, end):
				# Walk along the trie using the jth character
				# of the current word
				current = current.get_child(word[j])
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
	'''
	Finds the longest compound word in <words>
	composed of words in the passed-in trie.
	'''
	max_length = 0
	solution = ""
	for word in words:
		# We only evalaute whether a word is compound if it's
		# longer than the longest compound word found thus far.
		if len(word) > max_length and trie.isWordCompound(word):
			max_length = len(word)
			solution = word
	return solution

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print "Usage: python find_compound.py <filename>"
	else:		
		filename = sys.argv[1]
		trie = Trie(optimize_memory=False)
		words = []
		f = open(filename)
		for line in f:
			line = line.strip()
			trie.insert(line)
			words.append(line)

		start = time.time()
		print longestCompoundWord(trie, words)
		end = time.time()
		print "Finding longest compound word took %s seconds"%(end - start)