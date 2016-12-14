
from __future__ import division
import re
import os

class PriorityQueue:
	'''Implement priority queue using min-heap data structure'''
	def __init__(self,my_pq):
		self.pq = my_pq
		self.heapsize = 0 # keep track of heap size

	def insert(self, item): # item here is a tuple with the following format (state, path cost up to this state, order listed in input.txt)
		self.pq.append(item) # add item to end of queue
		self.heapsize += 1
		# Perform upheap to position the newly added node properly in the min-heap data structure
		self.upheap(self.heapsize)

	def upheap(self, heap_size):
		while heap_size // 2 > 0: # there is still a parent
			parent = heap_size // 2
			# compare the parent value to the child value. If child value is less than parent value, swap
			if self.pq[heap_size][1] < self.pq[parent][1]:
				self.pq[heap_size], self.pq[parent] = self.pq[parent], self.pq[heap_size]
			elif self.pq[heap_size][1] == self.pq[parent][1]:
				# in case of a tie, check the time stamp enqueue first to see when it is enqueued
				if self.pq[heap_size][5] < self.pq[parent][5]:
					self.pq[heap_size], self.pq[parent] = self.pq[parent], self.pq[heap_size]
				elif self.pq[heap_size][5] == self.pq[parent][5]:
					# in case of a tie in value and in time enqueue, check the order listed in input.txt to break ties
					if self.pq[heap_size][2] < self.pq[parent][2]:
						self.pq[heap_size], self.pq[parent] = self.pq[parent], self.pq[heap_size]

			heap_size = heap_size // 2 # update heap size to be parent and keep going upward

	def delMin(self):
		try:
			mymin = self.pq[1] # min path cost element is at top of queue
			# replace the min with last node
			self.pq[1] = self.pq[-1]
			# remove the last node in queue
			self.pq.pop()
			self.heapsize -= 1
			# Perform downheap to place the root in proper position in min heap
			self.downheap(1) # start to downheap at root (index 1 in heap)
			return mymin
		except IndexError:
			print "Min heap does not have any root"

	def downheap(self, parent):
		while(parent << 1) <= self.heapsize: # while there is a children
			minchild_index = self.findMinChild(parent)
			# compare the smaller child to the current parent. If parent is larger than the smaller child, swap
			if self.pq[parent][1] > self.pq[minchild_index][1]:
				self.pq[parent], self.pq[minchild_index] = self.pq[minchild_index], self.pq[parent]
			elif self.pq[parent][1] == self.pq[minchild_index][1]:
				# in case of a tie between parent and its mind child, check the time qneue
				if self.pq[parent][5] > self.pq[minchild_index][5]:
					self.pq[parent], self.pq[minchild_index] = self.pq[minchild_index], self.pq[parent]
				elif self.pq[parent][5] == self.pq[minchild_index][5]:
					# in case of a tie between the parent and its min child in value and time enqueue, check the order to break ties
					if self.pq[parent][2] > self.pq[minchild_index][2]:
						self.pq[parent], self.pq[minchild_index] = self.pq[minchild_index], self.pq[parent]

			parent = minchild_index

	def findMinChild(self, parent):
		if (parent << 1) + 1 > self.heapsize: # there is no right child. Return left child
			return (parent << 1)
		else:
			# Compare the 2 children and return the smaller one
			if self.pq[parent<<1][1] < self.pq[(parent<<1)+1][1]:
				return (parent<<1)
			elif self.pq[parent<<1][1] == self.pq[(parent<<1)+1][1]:
				# in case of a tie between two children, first check the time it is enqueued
				if self.pq[parent<<1][5] < self.pq[(parent<<1)+1][5]:
					return (parent<<1)
				elif self.pq[parent<<1][5] > self.pq[(parent<<1)+1][5]:
					return (parent<<1)+1
				elif self.pq[parent<<1][5] == self.pq[(parent<<1)+1][5]:
					# in case of a tie between two children in value and time enqeue, check the order to break ties
					if self.pq[parent<<1][2] < self.pq[(parent<<1)+1][2]:
						return (parent<<1)
					else:
						return (parent<<1)+1
			else:
				return (parent<<1)+1

	def replace_item(self, index, item):
		# swap the value of index in heap with new item
		self.pq[index] = item
		# Check if we need to upheap or downheap
		hasDoneUpheap = 0
		if index // 2 > 0:
			parent = index // 2
			# check if value at index is less than that of parent
			if self.pq[index][1] < self.pq[parent][1]:
				# we will perform upheap
				self.upheap(index)
				hasDoneUpheap = 1
			elif self.pq[index][1] == self.pq[parent][1]:
				# in case of a tie, check the time enqueue first
				if self.pq[index][5] < self.pq[parent][5]:
					self.upheap(index)
					hasDoneUpheap = 1
				elif self.pq[index][5] == self.pq[parent][5]:
					# in case of a tie in value and time enqueue, check order to break ties
					if self.pq[index][2] < self.pq[parent][2]:
						self.upheap(index)
						hasDoneUpheap = 1
		
		if (index << 1) <= self.heapsize and hasDoneUpheap == 0:
			# index has at least 1 children
			self.downheap(index)

	def find_item_index(self, item):
		for index in xrange(1, len(self.pq)):
			if self.pq[index][0] == item[0]: # has same state, return its index
				return index
		return None # return None if item is not in queue

	def printPriorityQueue(self):
		print self.pq

class SearchAlgr:
	def __init__(self, input_filename):
		self.inputFile = input_filename
		self.algr = ""
		self.start_state = ""
		self.gold_state = ""
		self.num_traffic_live = 0
		self.live_traffic_dict = {}
		self.num_sunday_traffic = 0
		self.sunday_traffic_dict = {}

	def parse_input(self):
		try:
			with open(self.inputFile, 'r') as fr:
				# we will go through file line by line based on input file format specified in HW1
				temp_num_traffic_count = 0
				temp_sunday_traffic_count = 0
				timestamp_count = 0
				for line in fr:
					if self.algr == "":
						self.algr = line.rstrip('\n')
						continue
					if self.start_state == "":
						self.start_state = line.rstrip('\n')
						continue
					if self.gold_state == "":
						self.gold_state = line.rstrip('\n')
						continue
					if self.num_traffic_live == 0:
						self.num_traffic_live = int(line)
						temp_num_traffic_count = self.num_traffic_live
						continue
					if temp_num_traffic_count > 0:
						line_split = re.split(r'\s+', line)
						# safe check to ensure we don't add duplicate items
						if not line_split[0] in self.live_traffic_dict:
							self.live_traffic_dict[line_split[0]] = []
							self.live_traffic_dict[line_split[0]].append( (line_split[1], int(line_split[2]), timestamp_count) )
						else:
							self.live_traffic_dict[line_split[0]].append( (line_split[1], int(line_split[2]), timestamp_count) )
						timestamp_count += 1
						temp_num_traffic_count -= 1
					else:
						if self.num_sunday_traffic == 0:
							self.num_sunday_traffic = int(line)
							temp_sunday_traffic_count = self.num_sunday_traffic
							continue
						else:
							if temp_sunday_traffic_count > 0:
								line_split = re.split(r'\s+', line)					
								# safe check to ensure we don't add duplicate items
								if not line_split[0] in self.sunday_traffic_dict:
									self.sunday_traffic_dict[line_split[0]] = int(line_split[1])
								temp_num_traffic_count -= 1
				# print to debug
				print "my algr = %s, start state = %s, gold state = %s, num_sunday_traffic = %d, num_sunday_traffic = %d\n" % (self.algr, self.start_state, self.gold_state, self.num_traffic_live, self.num_sunday_traffic)
				print self.live_traffic_dict
				print self.sunday_traffic_dict

		except IOError:
			print "There is no input file name %s or can't read it" % (self.inputFile)

	def search_use_BFS(self):
		'''Implement BFS to find path from given start to given gold
		I am utilizing queue data structure to perform FIFO for enqueuing function'''
		queue = [(self.start_state, [self.start_state])] # initialize the queue with tuple (state, path_to_state)
		visited = [self.start_state]
		while queue: # while queue is not empty
			# perform FIFO
			print queue
			(node, path) = queue.pop(0) # take out the first element in queue
			visited.append(node)
			# check if node is gold. If so, return since we are done
			if node == self.gold_state:
				return path
			# sanity check if node has any children. If it does not, simply skip
			if not node in self.live_traffic_dict:
				continue
			# if node is not gold, enqueue each of its children in the order listed in input file.
			# Careful to not include those that are already in the path to void loop
			for child in self.live_traffic_dict[node]:
				# ensure that we don't add duplicate entry in queue
				duplicate_entry_found = 0
				for state in queue:
					if child[0] == state[0]:
						duplicate_entry_found = 1
						break

				if not child[0] in visited and duplicate_entry_found == 0:
					queue.append( (child[0], path+[child[0]]) )
		return None # queue is empty and we still can't find path to gold. Return failure

	def search_use_DFS(self):
		''' Implement DFS to find path from given start to given gold
		I am utilizing stack data structure to perform LIFO for enqueuing function '''
		stack = [(self.start_state, [self.start_state])] # initialize the queue with tuple (state, path_to_state)
		visited = [self.start_state]
		while stack: # while stack is not empty
			# perform LIFO
			print stack
			(node, path) = stack.pop() # take out the last element in stack
			# print "explore node =" + node + "\n"
			visited.append(node)
			# check if node is gold. If so, return since we are done
			if node == self.gold_state:
				return path
			# sanity check if node has any children. If it does not, simply skip
			if not node in self.live_traffic_dict:
				continue
			# if node is not gold, enqueue each of its children in the order listed in input file.
			# Careful to not include those that are already in the path to void loop
			for child_index in xrange(len(self.live_traffic_dict[node])-1, -1, -1):
				# ensure that we don't add duplicate entry in stack
				duplicate_entry_found = 0
				for state in stack:
					if self.live_traffic_dict[node][child_index][0] == state[0]:
						duplicate_entry_found = 1
						break
				if not self.live_traffic_dict[node][child_index][0] in visited and duplicate_entry_found == 0:
					# print self.live_traffic_dict[node][child_index][0]
					stack.append( (self.live_traffic_dict[node][child_index][0], path+[ self.live_traffic_dict[node][child_index][0] ]) )
		return None # queue is empty and we still can't find path to gold. Return failure

	def search_use_UCS(self):
		''' Implment UCS to find path from given start to given gold
		I am utilizing priority queue to sort the queue based on path cost
		Priority Queue is implemented using heap data structure to keep min path cost element at root '''
		open_queue = [None] # initialize open_queue with None as first element with index = 0. In the heap implementation, we don't use the first index
		closed_queue = [] # empty list since we have not discovered any node yet

		timestamp_enqueue = 1

		# insert the start node with path cost 0 to open_queue to be explored
		myPQ = PriorityQueue(open_queue)
		myPQ.insert( (self.start_state, 0, 0, [self.start_state], [0], timestamp_enqueue) ) # tuple in format (state, path cost, order in input.txt, path, path cost at each state, timestampt node is enqueued)
		while len(open_queue) > 1: # we don't count the first element since it is None
			curnode = myPQ.delMin()
			print "my cur start node = %s, cur cost = %d, and path = %s" % (curnode[0], curnode[1], curnode[3])
			myPQ.printPriorityQueue()
			# Perform gold test on the curnode
			if curnode[0] == self.gold_state:
				print "Found gold with path %s " % curnode[3]
				return curnode

			# sanity check if node has any children. If it does not, simply skip
			if not curnode[0] in self.live_traffic_dict:
				# add to closed queue before continue
				print "Add curnode %s with path cost %d and path %s into CLOSED queue" % (curnode[0], curnode[1], curnode[3])
				closed_queue.append(curnode)
				continue
			
			timestamp_enqueue += 1
			# If it is not gold, explore its children
			for child in self.live_traffic_dict[curnode[0]]:
				index_child_in_open_queue = myPQ.find_item_index(child)
				index_child_in_close_queue = None
				for my_temp_index in xrange(0, len(closed_queue)):
					if closed_queue[my_temp_index][0] == child[0]:
						index_child_in_close_queue = my_temp_index
						break

				# check if this child is NOT in either OPEN or CLOSED queue. Then proceed to enqueue it into OPEN
				if index_child_in_open_queue == None and index_child_in_close_queue == None:
					print "child %s has never been explored. Add to open queue" % child[0]
					myPQ.insert( (child[0], int(child[1])+curnode[1], child[2], curnode[3]+[child[0]], curnode[4]+[int(child[1])], timestamp_enqueue) )
				elif index_child_in_open_queue != None:
					# child is already in the open queue to be explored, I need to check if there is a better path cost
					if int(child[1])+curnode[1] < open_queue[index_child_in_open_queue][1]: # if path cost to this child is less than what we know, update it in the open queue
						##### CHECK THIS PIECE OF CODE ABOVE TO SEE IF OPEN_QUEUE WORKS
						print "Found a child %s with path cost %d which is better than the node %s in open queue which has path cost %d" % (child[0], int(child[1])+curnode[1], open_queue[index_child_in_open_queue][0], open_queue[index_child_in_open_queue][1])
						myPQ.replace_item(index_child_in_open_queue, (child[0], int(child[1])+curnode[1], child[2], curnode[3]+[child[0]], curnode[4]+[int(child[1])], timestamp_enqueue) )
				elif index_child_in_close_queue != None:
					# child is already explored before, but somehow we find a better path to it. Update closed queue
					if int(child[1])+curnode[1] < closed_queue[index_child_in_close_queue][1]:
						# remove the node which has child state in closed queue
						print "Found a child which has better path cost than the node which has this child state in CLOSED queue"
						del closed_queue[index_child_in_close_queue]
						# Enqueue child into open queue
						myPQ.insert( (child[0], int(child[1])+curnode[1], child[2], curnode[3]+[child[0]], curnode[4]+[int(child[1])], timestamp_enqueue) )

			# insert curnode into closed queue since I have finished exploring it
			print "Add curnode %s with path cost %d and path %s into CLOSED queue" % (curnode[0], curnode[1], curnode[3])
			closed_queue.append(curnode)

		return None # queue is empty and we still can't find the path to gold. Return failure

	def search_use_Astar(self):
		''' Implment A* to find path from given start to given gold
		I am utilizing priority queue to sort the queue based on path cost
		Priority Queue is implemented using heap data structure to keep min path cost element at root '''
		open_queue = [None] # initialize open_queue with None as first element with index = 0. In the heap implementation, we don't use the first index
		closed_queue = [] # empty list since we have not discovered any node yet

		timestamp_enqueue = 1

		# insert the start node with path cost 0 to open_queue to be explored
		myPQ = PriorityQueue(open_queue)
		myPQ.insert( (self.start_state, 0 + self.sunday_traffic_dict[self.start_state], 0, [self.start_state], [0], timestamp_enqueue, 0) ) # tuple in format (state, path cost g(n) + h(n), order in input.txt, path, path cost at each state, time stamp enqueue, total path cost so far)
		while len(open_queue) > 1: # we don't count the first element since it is None
			curnode = myPQ.delMin()
			print "my cur start node = %s, cur cost = %d, and path = %s and total cost so far=%d" % (curnode[0], curnode[6], curnode[3], curnode[1])
			myPQ.printPriorityQueue()
			# Perform gold test on the curnode
			if curnode[0] == self.gold_state:
				print "Found gold with path %s " % curnode[3]
				return curnode

			# sanity check if node has any children. If it does not, simply skip
			if not curnode[0] in self.live_traffic_dict:
				# insert into closed queue before continue
				print "Add curnode %s with path cost %d and path %s into CLOSED queue" % (curnode[0], curnode[1], curnode[3])
				closed_queue.append(curnode)
				continue
			
			timestamp_enqueue += 1
			# If it is not gold, explore its children
			for child in self.live_traffic_dict[curnode[0]]:
				index_child_in_open_queue = myPQ.find_item_index(child)
				index_child_in_close_queue = None
				for my_temp_index in xrange(0, len(closed_queue)):
					if closed_queue[my_temp_index][0] == child[0]:
						index_child_in_close_queue = my_temp_index
						break

				# check if this child is NOT in either OPEN or CLOSED queue. Then proceed to enqueue it into OPEN
				if index_child_in_open_queue == None and index_child_in_close_queue == None:
					print "child %s has never been explored. Add to open queue" % child[0]
					myPQ.insert( (child[0], int(child[1])+curnode[6]+self.sunday_traffic_dict[child[0]], child[2], curnode[3]+[child[0]], curnode[4]+[int(child[1])], timestamp_enqueue, child[1]+curnode[6]) )
				elif index_child_in_open_queue != None:
					# child is already in the open queue to be explored, I need to check if there is a better path cost
					if int(child[1])+curnode[6]+self.sunday_traffic_dict[child[0]] < open_queue[index_child_in_open_queue][1]: # if path cost to this child is less than what we know, update it in the open queue
						##### CHECK THIS PIECE OF CODE ABOVE TO SEE IF OPEN_QUEUE WORKS
						print "Found a child %s with path cost %d which is better than the node %s in open queue which has path cost %d" % (child[0], int(child[1])+curnode[6]+self.sunday_traffic_dict[child[0]], open_queue[index_child_in_open_queue][0], open_queue[index_child_in_open_queue][1])
						myPQ.replace_item(index_child_in_open_queue, (child[0], int(child[1])+curnode[6]+self.sunday_traffic_dict[child[0]], child[2], curnode[3]+[child[0]], curnode[4]+[int(child[1])], timestamp_enqueue, child[1]+curnode[6]) )
				elif index_child_in_close_queue != None:
					# child is already explored before, but somehow we find a better path to it. Update closed queue
					if int(child[1])+curnode[6]+self.sunday_traffic_dict[child[0]] < closed_queue[index_child_in_close_queue][1]:
						# remove the node which has child state in closed queue
						print "Found a child %s which has better path cost=%d than the node %s which has this child state in CLOSED queue with path cost =%d" % (child[0], int(child[1])+curnode[6]+self.sunday_traffic_dict[child[0]], closed_queue[index_child_in_close_queue][0], closed_queue[index_child_in_close_queue][1])
						del closed_queue[index_child_in_close_queue]
						# Enqueue child into open queue
						myPQ.insert( (child[0], int(child[1])+curnode[6]+self.sunday_traffic_dict[child[0]], child[2], curnode[3]+[child[0]], curnode[4]+[int(child[1])], timestamp_enqueue,child[1]+curnode[6]) )

			# insert curnode into closed queue since I have finished exploring it
			print "Add curnode %s with path cost %d and path %s into CLOSED queue" % (curnode[0], curnode[1], curnode[3])
			closed_queue.append(curnode)

		return None # queue is empty and we still can't find the path to gold. Return failure

	def write_output_BFS_DFS(self, path):
		# remove any output.txt in current dir
		if os.path.isfile('output.txt'):
			os.remove('output.txt')
		count = 0 # path cost
		isFirst = True
		for element in path:
			with open ('output.txt', 'a+') as w:
				if isFirst:
					line = element + " " + str(count)
					isFirst = False;
				else:
					line = "\n" + element + " " + str(count)

				w.writelines(line)
			count += 1

	def write_output_UCS_A_star(self,path, path_cost):
		# remove any output.txt in current dir
		if os.path.isfile('output.txt'):
			os.remove('output.txt')
		isFirst = True
		total_path_cost = 0
		for index in xrange(0, len(path)):
			with open('output.txt', 'a+') as w:
				if isFirst:
					line = path[index] + " " + str(path_cost[index])
					total_path_cost += path_cost[index]
					isFirst = False
				else:
					total_path_cost += path_cost[index]
					line = "\n" + path[index] + " " + str(total_path_cost)
				w.writelines(line)


search = SearchAlgr('input_linux25.txt')
search.parse_input()

if search.algr == "BFS":
	bfs_path = search.search_use_BFS()
	print "my bfs search path = %s\n" % (bfs_path)
	search.write_output_BFS_DFS(bfs_path)
elif search.algr == "DFS":
	dfs_path = search.search_use_DFS()
	print "my dfs search path = %s\n" % (dfs_path)
	search.write_output_BFS_DFS(dfs_path)
elif search.algr == "UCS":
	ucs_path_info = search.search_use_UCS()
	print "my ucs search path = %s\n" % (ucs_path_info[3])
	search.write_output_UCS_A_star(ucs_path_info[3], ucs_path_info[4])
elif search.algr == "A*":
	Astar_path_info = search.search_use_Astar()
	print "my Astar search path = %s\n" % (Astar_path_info[3])
	search.write_output_UCS_A_star(Astar_path_info[3], Astar_path_info[4])