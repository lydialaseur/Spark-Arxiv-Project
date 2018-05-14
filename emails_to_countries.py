import argparse
import numpy as np
import json
import csv

parser = argparse.ArgumentParser(description="Convert a list of tuples into a JSON array")
parser.add_argument("sourcefile", help="Text file containing a list of email addresses")
parser.add_argument("destinationfile", help="Where to write the CSV mapping emails to countries")

def read_and_load_email_domains():
	"""
	Loads the JSON containing email domains and reformats it to a format more amenable to lookups
	"""
	with open("world_universities_and_domains.json") as json_file:
		raw_universities_json = json.loads(json_file)
		university_lookup = {}
		for university in raw_universities_json:
			for domain in university.get("domains"):

				university_summary = {}

				if university.get("name"):
					university_summary["name"] = university["name"]
				if university.get("country"):
					university_summary["country"] = university["country"]
				if university.get("alpha_two_code"):
					university_summary["alpha_two_code"] = university["alpha_two_code"]
				if university.get("state-province"):
					university_summary["state-province"] = university["state-province"]

				university_lookup[domain] = university_info

if __name__ == '__main__':
	args = parser.parse_args()

	university_lookup = read_and_load_email_domains()

	with open(args.sourcefile) as sourcefile:
		emails = sourcefile.readlines()

	email_csv = [("email", "domain", "institution", "country", "country_code", "province")]

	for email in emails:
		domain = email.split("@")[-1]
		if university_lookup.get(domain):
			university_info = university_lookup[domain]
			email_csv.append((email, 
				domain, 
				university_info.get("name"), 
				university_info.get("country"),
				university_info.get("alpha_two_code"),
				university_info.get("state-province")))

	with open(args.destinationfile, 'w') as destinationfile:
		writer = csv.writer(destinationfile)
		for row in email_csv:
			writer.writerow(row)
