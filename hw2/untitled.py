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

	def perform_reverse_action_made (self, state, player, action_type, action_made):
		'''Perform a reverse of all actions made earlier in the move'''
		if len(action_made) <= 0:
			return None

		for action in action_made:
			if action[2] == "Stake":
				state[action[0]][action[1]] = "."
			else: # It was a RAID move
				 # Now need to reverse those squares that had been conquered
				 state[action[0]][action[1]] = self.select_player( state[action[0]][action[1]] )