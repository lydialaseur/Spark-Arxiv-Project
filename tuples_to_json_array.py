import argparse
import numpy as np
import json

parser = argparse.ArgumentParser(description="Convert a list of tuples into a JSON array")
parser.add_argument("sourcefile", help="Text file containing a list of tuples")
parser.add_argument("destinationfile", help="Where to write the JSON containing those tuples as arrays")

def parse_row(row):
	"""
	Primitively parses a tuple that is formatted like this:
		('endogeny', 1)
	and returns a 2-element list like this:
		["endogeny", 1]
	"""
	word, count = row.split(",")
	word = word[2:-1]
	count = int(count[1:-2])
	return [word, count]

if __name__ == '__main__':
	args = parser.parse_args()
	with open(args.sourcefile, 'r') as sourcefile:
		values = [parse_row(row) for row in sourcefile.readlines()]
	with open(args.destinationfile, 'w') as destinationfile:
		json.dump(destinationfile, values)


