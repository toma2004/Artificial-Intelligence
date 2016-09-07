import re
import os

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

	def get_algr(self):
		return self.algr

	def parse_input(self):
		try:
			with open(self.inputFile, 'r') as fr:
				# we will go through file line by line based on input file format specified in HW1
				temp_num_traffic_count = 0
				temp_sunday_traffic_count = 0
				for line in fr:
					if self.algr == "":
						self.algr = line.rstrip('\n')
						print self.algr
						test = line.replace('\n', '')
						print test
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
							self.live_traffic_dict[line_split[0]].append((line_split[1], line_split[2]))
						else:
							self.live_traffic_dict[line_split[0]].append((line_split[1], line_split[2]))
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
									self.sunday_traffic_dict[line_split[0]] = line_split[1]
								temp_num_traffic_count -= 1
				# print to debug
				print "my algr = %s, start_state = %s, gold_state = %s, num_sunday_traffic = %d, num_sunday_traffic = %d\n" % (self.algr, self.start_state, self.gold_state, self.num_traffic_live, self.num_sunday_traffic)
				print self.algr
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
				if not child[0] in visited:
					queue.append( (child[0], path+[child[0]]) )
		return None # queue is empty and we still can't find path to gold. Return failure

	def search_use_DFS(self):
		''' Implement DFS to find path from given start to given gold
		I am utilizing stack data structure to perform LIFO for enqueuing function '''
		stack = [(self.start_state, [self.start_state])] # initialize the queue with tuple (state, path_to_state)
		visited = [self.start_state]
		while stack: # while stack is not empty
			# perform LIFO
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
				if not self.live_traffic_dict[node][child_index][0] in visited:
					# print self.live_traffic_dict[node][child_index][0]
					stack.append( (self.live_traffic_dict[node][child_index][0], path+[ self.live_traffic_dict[node][child_index][0] ]) )
		return None # queue is empty and we still can't find path to gold. Return failure

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

search = SearchAlgr('input3.txt')
search.parse_input()
myalgr = search.get_algr()
print myalgr + "test"

bfs_path = search.search_use_BFS()
print "my bfs search path = %s\n" % (bfs_path)
search.write_output_BFS_DFS(bfs_path)

if myalgr == "BFS":
	bfs_path = search.search_use_BFS()
	print "my bfs search path = %s\n" % (bfs_path)
	search.write_output_BFS_DFS(bfs_path)
elif myalgr == "DFS":
	dfs_path = search.search_use_DFS()
	print "my dfs search path = %s\n" % (dfs_path)
	search.write_output_BFS_DFS(dfs_path)