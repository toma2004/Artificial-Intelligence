import re
import sys
import os
import time
from operator import itemgetter
import math

class GamePlay:
	def __init__(self, input_file):
		self.input_file = input_file
		self.boardSize = 0
		self.mode = None
		self.player = None
		self.depth = 1
		self.cpuTime = 0
		self.cell_val = []
		self.boardState = []

	def parse_input(self):
		try:
			with open(self.input_file, 'r') as f:
				temp_N_count_cell_val = 0
				temp_N_count_board_state = 0
				row_cell_val = 0
				row_board_state = 0
				for line in f:
					if self.boardSize == 0:
						self.boardSize = int(line)
						temp_N_count_cell_val = self.boardSize
						# initialize cell value 2d array
						self.cell_val = [[None for x in range(self.boardSize)] for y in range(self.boardSize)]
						temp_N_count_board_state = self.boardSize
						# initialize board state 2d array
						self.boardState = [[None for x in range(self.boardSize)] for y in range(self.boardSize)]
						continue
					if self.mode == None:
						self.mode = line.rstrip('\n')
						continue
					if self.player == None:
						self.player = line.rstrip('\n')
						continue
					if self.cpuTime == 0:
						self.cpuTime = float(line)
						continue
					if temp_N_count_cell_val > 0:
						line_split = re.split(r'\s+', line)
						for i in range(self.boardSize):
							self.cell_val[row_cell_val][i] = int(line_split[i])
						row_cell_val += 1
						temp_N_count_cell_val -= 1
					elif temp_N_count_board_state > 0:
						line_split = list(line)
						for i in range(self.boardSize):
							self.boardState[row_board_state][i] = line_split[i]
						row_board_state += 1
						temp_N_count_board_state -= 1

				# print to debug
				#print "my N = %d, MODE = %s, YOUPLAY = %s, DEPTH = %d\n" % (self.boardSize, self.mode, self.player, self.depth)
				#print "my cell value =", self.cell_val
				#print "my board state = ", self.boardState 

		except IOError:
			print "There is no input file name %s or can't read it\n" % (self.input_file)

	def calculate_score(self, state):
		sum_x_score = 0
		sum_o_score = 0
		for i in range(self.boardSize):
			for j in range(self.boardSize):
				if state[i][j] == "X" or state[i][j] == "x":
					sum_x_score += self.cell_val[i][j]
				elif state[i][j] == "O" or state[i][j] == "o":
					sum_o_score += self.cell_val[i][j]
		# print "sum x score = %d" % sum_x_score
		# print "sum o score = %d" % sum_o_score

		if self.player == "X" or self.player == "x":
			return sum_x_score - sum_o_score
		else:
			return sum_o_score - sum_x_score

	def terminate_test(self, state):
		for i in range(self.boardSize):
			for j in range(self.boardSize):
				if state[i][j] == ".":
					return False
		return True

	def isRaid_move(self, state, move, player):
		'''Given a list of all possible moves, classify which move could be a Raid.
		A qualified Raid move needs to have at least 1 adjacent square to be the player's square and at least 1 adjacent square to be the opponent's square
		'''
		#print "state in isRaid_move = %s and player = %s\n" % (state, player)
		foundPlayerSquare = 0
		foundOpponentSquare = 0
		score_after_acquired = 0

		#print "my current MOVE = %s\n" % (move)
		if (move[0]-1) >= 0:
			if player == "X" or player == "x":		
				if state[move[0]-1][move[1]] == "X" or state[move[0]-1][move[1]] == "x":
					#print "found player square at 1 - X"
					foundPlayerSquare = 1
				elif state[move[0]-1][move[1]] == "O" or state[move[0]-1][move[1]] == "o":
					foundOpponentSquare = 1
					score_after_acquired += self.cell_val[move[0]-1][move[1]]
					#print "found opponent square at 1 - O"
			else:
				if state[move[0]-1][move[1]] == "X" or state[move[0]-1][move[1]] == "x":
					foundOpponentSquare = 1
					score_after_acquired += self.cell_val[move[0]-1][move[1]]
					#print "found opponent square at 1 - X"
				elif state[move[0]-1][move[1]] == "O" or state[move[0]-1][move[1]] == "o":
					foundPlayerSquare = 1
					#print "found player square at 1 - O"

		if (move[0]+1) <= self.boardSize-1:
			if player == "X" or player == "x":
				if state[move[0]+1][move[1]] == "X" or state[move[0]+1][move[1]] == "x":
					#print "found player square at 2 - X"
					foundPlayerSquare = 1
				elif state[move[0]+1][move[1]] == "O" or state[move[0]+1][move[1]] == "o":
					foundOpponentSquare = 1
					score_after_acquired += self.cell_val[move[0]+1][move[1]]
					#print "found opponent square at 2 - O"
			else:
				if state[move[0]+1][move[1]] == "X" or state[move[0]+1][move[1]] == "x":
					foundOpponentSquare = 1
					score_after_acquired += self.cell_val[move[0]+1][move[1]]
					#print "found opponent square at 2 - X"
				elif state[move[0]+1][move[1]] == "O" or state[move[0]+1][move[1]] == "o":
					foundPlayerSquare = 1
					#print "found player square at 2 - O"

		if (move[1]-1) >= 0:
			if player == "X" or player == "x":
				if state[move[0]][move[1]-1] == "X" or state[move[0]][move[1]-1] == "x":
					#print "found player square at 3 - X"
					foundPlayerSquare = 1
				elif state[move[0]][move[1]-1] == "O" or state[move[0]][move[1]-1] == "o":
					foundOpponentSquare = 1
					score_after_acquired += self.cell_val[move[0]][move[1]-1]
					#print "found opponent square at 3 - O"
			else:
				if state[move[0]][move[1]-1] == "X" or state[move[0]][move[1]-1] == "x":
					foundOpponentSquare = 1
					score_after_acquired += self.cell_val[move[0]][move[1]-1]
					#print "found opponent square at 3 - X"
				elif state[move[0]][move[1]-1] == "O" or state[move[0]][move[1]-1] == "o":
					foundPlayerSquare = 1
					#print "found player square at 3 - O"

		if (move[1]+1) <= self.boardSize-1:
			if player == "X" or player == "x":
				if state[move[0]][move[1]+1] == "X" or state[move[0]][move[1]+1] == "x":
					#print "found player square at 4 - X"
					foundPlayerSquare = 1
				elif state[move[0]][move[1]+1] == "O" or state[move[0]][move[1]+1] == "o":
					foundOpponentSquare = 1
					score_after_acquired += self.cell_val[move[0]][move[1]+1]
					#print "found opponent square at 4 - O"
			else:
				if state[move[0]][move[1]+1] == "X" or state[move[0]][move[1]+1] == "x":
					foundOpponentSquare = 1
					score_after_acquired += self.cell_val[move[0]][move[1]+1]
					#print "found opponent square at 4 - X"
				elif state[move[0]][move[1]+1] == "O" or state[move[0]][move[1]+1] == "o":
					foundPlayerSquare = 1
					#print "found player square at 4 - O"

		if foundPlayerSquare and foundOpponentSquare:
			# this move is qualified as Raid move. Modify it in the move_list
			#print "change move = %s to RAID" % (move)
			return (True, score_after_acquired)

		return (False, score_after_acquired)

	def get_actions(self, state, player):
		''' Get all available action given a state and return a list'''
		available_move = []
		raid_move = []
		stake_move = []
		for i in range(self.boardSize):
			for j in range(self.boardSize):
				if state[i][j] == ".":
					# check if it is a Raid move
					isRaid = self.isRaid_move(state, [i, j], player)
					if isRaid[0]:
						#available_move.append( [i, j, "Raid"] )
						raid_move.append( [i, j, "Raid", isRaid[1] ] )
						#print "RAID SCORE = %d\n" % isRaid[1]
					else:	
						#available_move.append( [i, j, "Stake"] )
						stake_move.append( [i, j, "Stake", self.cell_val[i][j] ] )

		# sort stake move in descending order of state[i][j] value
		sorted_stake_move = sorted(stake_move, key=itemgetter(3), reverse=True)
		#print "my sorted stake move = ", sorted_stake_move

		if raid_move:
			# sorted raid move in descending order in term of score acquired
			sorted_raid_move = sorted(raid_move, key=itemgetter(3), reverse=True)
			#print "my sorted raid move = ", sorted_raid_move

			# Put Raid move if any to about 1/3 of the sorted stake move
			index = int(math.floor(len(sorted_stake_move) / 4))
			#print "my index = %d and type = %s\n" % (index, type(index))
			#print "add RAID move\n"

			available_move = sorted_stake_move[:index] + sorted_raid_move + sorted_stake_move[index:]
			#print "available move = ", available_move
			
			return available_move

		# Now go through each available move list to re-consider which of them could be qualified as Raid move
		#self.isRaid_move(state, available_move, player)

		return sorted_stake_move

	def perform_action(self, state, player, action):
		'''given an action, modify the state to reflect the action and return the list of actions taken'''
		action_made = []
		if action[2] == "Stake":
			if player == "X" or player == "x":
				state[action[0]][action[1]] = "X"
			else:
				state[action[0]][action[1]] = "O"
			action_made.append( (action[0], action[1], "Stake") )
		else: # move is Raid
			if player == "X" or player == "x":
				state[action[0]][action[1]] = "X"
				action_made.append( (action[0], action[1], "Stake") )
				# Now need to turn those oppenent's squares touching this move to be the player's square
				# Check top
				if action[0]-1 >= 0:
					if state[action[0]-1][action[1]] == "O" or state[action[0]-1][action[1]] == "o":
						state[action[0]-1][action[1]] = "X"
						action_made.append( (action[0]-1, action[1], "Raid") )
				# Check bottom
				if action[0]+1 <= self.boardSize-1:
					if state[action[0]+1][action[1]] == "O" or state[action[0]+1][action[1]] == "o":
						state[action[0]+1][action[1]] = "X"
						action_made.append( (action[0]+1, action[1], "Raid") )
				# Check left
				if action[1]-1 >= 0:
					if state[action[0]][action[1]-1] == "O" or state[action[0]][action[1]-1] == "o":
						state[action[0]][action[1]-1] = "X"
						action_made.append( (action[0], action[1]-1, "Raid") )
				# check right
				if action[1]+1 <= self.boardSize-1:
					if state[action[0]][action[1]+1] == "O" or state[action[0]][action[1]+1] == "o":
						state[action[0]][action[1]+1] = "X"
						action_made.append( (action[0], action[1]+1, "Raid") )
			else: # player is O
				state[action[0]][action[1]] = "O"
				action_made.append( (action[0], action[1], "Stake") )
				# Now need to turn those oppenent's squares touching this move to be the player's square
				# Check top
				if action[0]-1 >= 0:
					if state[action[0]-1][action[1]] == "X" or state[action[0]-1][action[1]] == "x":
						state[action[0]-1][action[1]] = "O"
						action_made.append( (action[0]-1, action[1], "Raid") )
				# Check bottom
				if action[0]+1 <= self.boardSize-1:
					if state[action[0]+1][action[1]] == "X" or state[action[0]+1][action[1]] == "x":
						state[action[0]+1][action[1]] = "O"
						action_made.append( (action[0]+1, action[1], "Raid") )
				# Check left
				if action[1]-1 >= 0:
					if state[action[0]][action[1]-1] == "X" or state[action[0]][action[1]-1] == "x":
						state[action[0]][action[1]-1] = "O"
						action_made.append( (action[0], action[1]-1, "Raid") )
				# check right
				if action[1]+1 <= self.boardSize-1:
					if state[action[0]][action[1]+1] == "X" or state[action[0]][action[1]+1] == "x":
						state[action[0]][action[1]+1] = "O"
						action_made.append( (action[0], action[1]+1, "Raid") )
		return action_made

	def perform_reverse_action_made (self, state, action_made):
		'''Perform a reverse of all actions made earlier in the move'''
		if len(action_made) <= 0:
			return None

		for action in action_made:
			if action[2] == "Stake":
				state[action[0]][action[1]] = "."
			else: # It was a RAID move
				 # Now need to reverse those squares that had been conquered
				 state[action[0]][action[1]] = self.select_player( state[action[0]][action[1]] )


	def select_player(self, current_player):
		if current_player == "X" or current_player == "x":
			return "O"
		return "X"

	def run_minimax_alphaBeta(self, state, cpuTime, player, alpha, beta):
		'''Function to run minimax algorithm with alpha-beta pruning technique and select the best optimal move for player'''
		max_score = -sys.maxint-1

		actions = self.get_actions(state, player)
		#print "all available move =", actions

		# calculate maximum time for my move in order to make it with all actions
		allowedTime = cpuTime / (len(actions) / 2.0)
		print "cputime = %f and divide by len of actions = %d, my allowed time = %f\n" % (cpuTime, len(actions) ,allowedTime)

		max_action = None

		score_and_action = (0, None)

		# time per action
		time_per_action = allowedTime / len(actions)
		print "time per action = %f\n" % (time_per_action)

		for action in actions:

			action_made = self.perform_action(state, player, action)
			# print "action taken ROOT = ", action
			# print "current board state ROOT = ", state
			# print "player ROOT = %s" % (player)

			temp_score = self.minimax_min_move_alphaBeta(state, time_per_action, self.select_player(player), alpha, beta)

			if temp_score > max_score:
				max_score = temp_score
				max_action = action
			elif temp_score == max_score: #in case of tie, use the action to break tie
				test_action = self.getMax(action, max_action)
				if test_action == action:
					max_action = action

			# print "max score return in ROOT = ", max_score
			# print "max action being run in ROOT = ", max_action

			self.perform_reverse_action_made(state, action_made)


		#print "my max action is ", max_action
		return max_action		


	def minimax_max_move_alphaBeta(self, state, allowedTime, player, alpha, beta):
		'''Max function to return the max possible value for the move to be made by player'''
		# Cut-off search or terminal search
		#print "max depth = %d" % depth
		epsilon = 0.0001
		if (allowedTime-epsilon) <= 0 or self.terminate_test(state):
			return self.calculate_score(state)

		# initialize v to be some min int and lowest priority in all possible moves
		v = -sys.maxint - 1

		actions = self.get_actions(state, player)
		#print "all acttions in max = ", actions

		time_per_action = allowedTime / len(actions)

		for action in actions:
			# perform action on the current board state
			action_made = self.perform_action(state, player, action)

			# print "action taken in MAX = ", action
			# print "current board state in MAX = ", state
			# print "player in MAX = %s" % (player)

			v = max(v, self.minimax_min_move_alphaBeta(state, time_per_action, self.select_player(player), alpha, beta) )

			# Perform reverse action made earlier to prepare for next test
			self.perform_reverse_action_made(state, action_made)

			# in Max move, we check against beta to see if v > Beta
			# If so, we end early since the Min function will pick Beta
			if v >= beta:
				return v

			# update alpha
			alpha = max(v, alpha)

			#print "board state after getMax = ", state

			#print "my v return in MAX = ", v

		return v

	def minimax_min_move_alphaBeta(self, state, allowedTime, player, alpha, beta):
		'''Min function to return the min possible value for the move to be made by player'''
		# Cut-off search or terminal search
		#print "min depth = %d" % depth
		epsilon = 0.0001
		if (allowedTime-epsilon) <= 0 or self.terminate_test(state):
			return self.calculate_score(state)

		# initialize v to be some min int and lowest priority in all possible moves
		v = sys.maxint

		actions = self.get_actions(state, player)
		#print "all acttions in MIN = ", actions

		time_per_action = allowedTime / len(actions)

		for action in actions:
			# perform action on the current board state
			action_made = self.perform_action(state, player, action)

			# print "action taken MIN = ", action
			# print "current board state MIN = ", state
			# print "player MIN = %s" % (player)

			v = min(v, self.minimax_max_move_alphaBeta(state, time_per_action, self.select_player(player), alpha, beta) )

			# Perform reverse action made earlier to prepare for next test
			self.perform_reverse_action_made(state, action_made)

			# in Min move, we check against alpha to see if v < alpha
			# If so, we end early since Max function will pick alpha
			if v <= alpha:
				return v

			# update beta
			beta = min(v, beta)

			#print "board state after MIN = ", state

			#print "my v return MIN = ", v

		#print "\nMY FINAL RETURN IN MIN FUNCTION v = \n", v

		return v

	def getMax(self, action1, action2):
		'''compare two actions to break tie since they both give same score'''
		if action1[2] == "Stake" and action2[2] != "Stake": # we prioritize Stake action over Raid
			return action1
		elif action1[2] != "Stake" and action2[2] == "Stake":
			return action2
		else: # both are Stake or Raid
			# Now need to compare which one appears first in the board in the order top left -> bottom right
			if action1[0] < action2[0]: # appear in previous row
				return action1
			elif action1[0] == action2[0]: # appear on same row, need to check col
				if action1[1] < action2[1]:
					return action1
				else:
					return action2
			else:
				return action2

	def write_output(self, state, max_action, player):
		# table look up to name column in alphabetic order
		lookup_table = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
		# remove any output.txt in current dir
		if os.path.isfile('output.txt'):
			os.remove('output.txt')

		with open('output.txt', 'a+') as w:
			line = lookup_table[max_action[1]] + str(max_action[0]+1) + " " + max_action[2]
			w.writelines(line)
			# perform max action on state before print
			self.perform_action(state, player, max_action)
			for i in range(self.boardSize):
				w.writelines("\n")
				for j in range(self.boardSize):
					w.writelines(state[i][j])

#mygame = GamePlay("TestCasesHW2/TestCasesHW2/Test10/input.txt")
mygame = GamePlay("input.txt")

mygame.parse_input()
#print "my board state outside class =", mygame.boardState
#print "my depth = %d, my player = %s\n" % (mygame.depth, mygame.player)


###### Calculate time to completion #####
start = time.clock()

max_action = None
max_action = mygame.run_minimax_alphaBeta(mygame.boardState, mygame.cpuTime, mygame.player, -sys.maxint-1, sys.maxint)
# write result to output.txt
mygame.write_output(mygame.boardState, max_action, mygame.player)

###### End time #####
print time.clock() - start, " seconds elapsed\n"
