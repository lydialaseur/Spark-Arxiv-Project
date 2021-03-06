import argparse
import numpy as np
import json
import csv

parser = argparse.ArgumentParser(description="Convert a list of tuples into a JSON array")
parser.add_argument("sourcefile", help="Text file containing a list of email addresses")
parser.add_argument("destinationfile_matched", help="Where to write the CSV mapping emails to countries")
parser.add_argument("dest_unmatched_addresses", help="Where to write the email addresses that were not matched to a univerity")
parser.add_argument("dest_unmatched_domains", help="Where to write the email domains that were not matched to a univerity")

def read_and_load_email_domains():
	"""
	Loads the JSON containing email domains and reformats it to a format more amenable to lookups
	"""
	with open("world_universities_and_domains.json") as json_file:
		raw_json_text = json_file.read()

	raw_universities_json = json.loads(raw_json_text)
	university_lookup = {}
	for university in raw_universities_json:
		# print(university)
		# input()
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

			university_lookup[domain] = university_summary

	return(university_lookup)

if __name__ == '__main__':
	args = parser.parse_args()

	university_lookup = read_and_load_email_domains()

	unmatched_domains = [("document_id","email_domain")]
	unmatched_addresses = [("document_id","email_address")]
	with open(args.sourcefile) as sourcefile:
		docs_emails = sourcefile.readlines()

	email_csv = [("document_id", "email", "domain", "institution", "country", "country_code", "province")]

	for row in docs_emails:
		doc_id, email = row.split(",")

		email = email.strip()

		if email[-1] == ".":
			email = email[0:len(email) - 1]

		domain = email.split("@")[-1]

		match_found = False
		while domain:
			domain_lookup = university_lookup.get(domain)
			if domain_lookup:
				university_info = university_lookup[domain]
				email_csv.append((doc_id,
					email,
					domain,
					university_info.get("name"),
					university_info.get("country"),
					university_info.get("alpha_two_code"),
					university_info.get("state-province")))
				match_found = True
				break
			else:
				domain = domain.partition(".")[-1]


		if match_found == False:

			unmatched_domains.append((doc_id,email.split("@")[-1]))
			unmatched_addresses.append((doc_id,email))

	print()
	print("Total number of email addresses: {0}".format(len(docs_emails)))
	print("Number of email addresses matched to a university: {0}".format(len(email_csv)))
	print("Number of email addresses not matched to a university: {0}".format(len(unmatched_addresses)))
	print()

	with open(args.destinationfile_matched, 'w') as destinationfile_matched:
		writer = csv.writer(destinationfile_matched)
		for row in email_csv:
			writer.writerow(row)

	with open(args.dest_unmatched_addresses, 'w') as dest_unmatched_addresses:
		writer = csv.writer(dest_unmatched_addresses)
		for row in unmatched_addresses:
			writer.writerow(row)


	with open(args.dest_unmatched_domains, 'w') as dest_unmatched_domains:
		writer = csv.writer(dest_unmatched_domains)
		for row in unmatched_domains:
			writer.writerow(row)
