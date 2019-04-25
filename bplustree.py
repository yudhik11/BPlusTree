from __future__ import print_function
import sys, time, os
import numpy as np
import bisect


class Node:
	def __init__(self):
		self.keys = []
		self.children = []
		self.next = None
		self.isleaf = True

	def split(self):
		temp_node = Node()
		temp_node.isleaf = self.isleaf
		mid = len(self.keys) // 2
		mid_value = self.keys[mid]
		
		if not self.isleaf:
			temp_node.keys = self.keys[mid+1:]
			self.keys = self.keys[:mid]
			
			temp_node.children = self.children[mid+1:]
			self.children = self.children[:mid+1]
			
		else:
			temp_node.keys = self.keys[mid:]
			self.keys = self.keys[:mid]

			temp_node.children = self.children[mid:]
			self.children = self.children[:mid]

			temp_node.next = self.next
			self.next = temp_node

		return mid_value, temp_node


class BPlusTree(Node):
	def __init__(self, capacity):
		self.capacity = capacity
		self.root = Node()
	
	def range_query(self, min_val, max_val):
		ret = 0
		start = self.get_start_leaf(min_val, self.root)
		curr_node = start

		while curr_node is not None:
			count_curr_node, curr_node = self.keys_in_range(min_val, max_val, curr_node)
			ret += count_curr_node

		return ret
	
	def insert(self, value, node):
		if not node.isleaf:
			for i in range(len(node.keys)):
				if i is 0 and value < node.keys[i]:
					mid_value, new = self.insert(value, node.children[0])
					break
				if i is (len(node.keys) - 1):
					if value < node.keys[i]:
						continue
					else :
						mid_value, new = self.insert(value, node.children[-1])
						break
				if(value >= node.keys[i]):
					if (value<node.keys[i+1]):
						mid_value, new = self.insert(value, node.children[i+1])
						break
			
		else:
			idx = bisect.bisect(node.keys, value)
			node.keys.insert(idx, value)
			node.children.insert(idx, value)

			if len(node.keys) > self.capacity:
				return node.split()
			else:
				return None, None

		if mid_value:
			idx = bisect.bisect(node.keys, mid_value)
			node.keys.insert(idx, mid_value)
			node.children.insert(idx+1, new)
			if len(node.keys) <= self.capacity:
				return None, None
			else:
				return node.split()
		else:
			return None, None

	def insert_op(self, value):
		mid_value, new_node = self.insert(value, self.root)
		if mid_value:
			new_root = Node()
			new_root.children = [self.root, new_node]
			new_root.keys = [mid_value]
			new_root.isleaf = False
			self.root = new_root

	def get_start_leaf(self,val, node):
		if(node.isleaf):
			return node

		for i in range(len(node.keys)):
			if i == 0 and val <= node.keys[0]:
					return self.get_start_leaf(val, node.children[0])

			if i == (len(node.keys) - 1):
				if val <= node.keys[-1]:
					continue
				else:	
					return self.get_start_leaf(val, node.children[-1])

			
			if val > node.keys[i]:
				if val <= node.keys[i+1]:
					return self.get_start_leaf(val, node.children[i+1])

	def keys_in_range(self, min_val, max_val, node):
		ret=0
		if(len(node.keys) == 0):
			return 0, None

		for i in range(len(node.keys)):
			if node.keys[i] >= min_val:
				if  node.keys[i] <= max_val:
					ret+=1

		if node.keys[-1] > max_val:
			return ret, None
		else:
			return ret, node.next


	

def execute(cmd):
	global output_buffer

	if(cmd[0] == "RANGE"):
		out = tree.range_query(int(cmd[1]), int(cmd[2]))
		output_buffer.append(str(out))
	elif(cmd[0] == "INSERT"):
		tree.insert_op(int(cmd[1]))
	elif(cmd[0] == "COUNT"):
		out = tree.range_query(int(cmd[1]), int(cmd[1]))
		output_buffer.append(str(out))
	elif(cmd[0] == "FIND"):
		out = tree.range_query(int(cmd[1]), int(cmd[1]))
		if out == 0:
			output_buffer.append("NO")
		else:
			output_buffer.append("YES")
	
	if len(output_buffer) >= ((B * 1.0) / 10.0):
		for out in output_buffer:
			print(out)
		output_buffer = []

def main():
	# print(file, M, B, capacity)
	global output_buffer
	input_buffer = []
	with open(file, 'r') as f:
		for line in f:
			line = line.strip().split()
			input_buffer.append(line)
			
			if len(input_buffer) >= M-1:
				for cmd in input_buffer:
					execute(cmd)
				input_buffer = []

		if len(input_buffer):
			for cmd in input_buffer:
				execute(cmd)
		input_buffer = []

	for res in output_buffer:
		print(res)
	output_buffer = []

output_buffer = list()

if __name__ == "__main__":
	if len(sys.argv) != 4:
		sys.exit("Usage: python file.py input_file M B")
	
	args = sys.argv
	file = args[1]
	M = int(args[2])
	B = int(args[3])
	# global input_buffer
	# input_buffer = []
	capacity = B - 8 // 12
	pointers = capacity+1

	if(M<2):
		sys.exit("M should be greater than or equal to 2")
	if(B<20):
		sys.exit("Insufficient size for node")
	if (M*B > 1000000):
		sys.exit("M * B should be less than 1000000")
	if pointers < 2:
		pointers = 2
	
	tree = BPlusTree(capacity)
	main()