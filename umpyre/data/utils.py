"""
Utilities for applying formatting, aggregating, etc.
operations.
"""

def code_batting_direction(player_name):
	if '*' in player_name:
		return player_name.replace('*',''), 'L'  # left
	elif '#' in player_name:
		return player_name.replace('#',''), 'B'  # both
	elif '?' in player_name:
		return player_name.replace('?',''), 'U'  # right
	else:
		return player_name.strip(), 'R'  # unknown


def code_pitching_direction(player_name):
	return code_batting_direction(player_name)