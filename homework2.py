import re

def parse_input(input_filename):
	try:
		with open(input_filename, 'r') as fr:
			# Define and initialize necessary variables
			algr = ""
			start_state = ""
			gold_state = ""
			num_traffic_live = 0
			live_traffic_dict = {}
			num_sunday_traffic = 0
			sunday_traffic_dict = {}

			# we will go through file line by line based on input file format specified in HW1
			temp_num_traffic_count = 0
			temp_sunday_traffic_count = 0
			for line in fr:
				if algr == "":
					algr = line
					continue
				if start_state == "":
					start_state = line
					continue
				if gold_state == "":
					gold_state = line
					continue
				if num_traffic_live == 0:
					num_traffic_live = int(line)
					temp_num_traffic_count = num_traffic_live
					continue
				if temp_num_traffic_count > 0:
					line_split = re.split(r'\s+', line)
					# safe check to ensure we don't add duplicate items
					if not line_split[0] in live_traffic_dict:
						live_traffic_dict[line_split[0]] = {}
						live_traffic_dict[line_split[0]][line_split[1]] = line_split[2]
					else:
						live_traffic_dict[line_split[0]][line_split[1]] = line_split[2]
					temp_num_traffic_count -= 1
				else:
					if num_sunday_traffic == 0:
						num_sunday_traffic = int(line)
						temp_sunday_traffic_count = num_sunday_traffic
						continue
					else:
						if temp_sunday_traffic_count > 0:
							line_split = re.split(r'\s+', line)					
							# safe check to ensure we don't add duplicate items
							if not line_split[0] in sunday_traffic_dict:
								sunday_traffic_dict[line_split[0]] = line_split[1]
							temp_num_traffic_count -= 1
			# print to debug
			print "my algr = %s, start_state = %s, gold_state = %s, num_sunday_traffic = %d, num_sunday_traffic = %d\n" % (algr, start_state, gold_state, num_traffic_live, num_sunday_traffic)
			print live_traffic_dict
			print sunday_traffic_dict

	except IOError:
		print "There is no input file name %s or can't read it" % (input_filename)

parse_input('input.txt')