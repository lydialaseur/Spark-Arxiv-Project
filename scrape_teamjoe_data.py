import csv

with open("all_article_data_2.txt", "r") as infile:
    arxiv_data = infile.readlines()


ids_and_cats = [("document_id", "main_category", "sub_category")]

for row in arxiv_data:
    data = row.split("@@@")
    doc_id = data[0].split(".")[1][0:5]
    primary_category_parts = data[6].split(":")[1].strip().split(".")
    if len(primary_category_parts) == 1:
        doc_main_category = primary_category_parts[0]
        doc_sub_category = ""
    elif len(primary_category_parts) == 2:
        doc_main_category, doc_sub_category = primary_category_parts

    # print(doc_id)
    # print(doc_primary_category)
    # input()
    ids_and_cats.append((doc_id, doc_main_category, doc_sub_category))

with open("arxiv_ids_categories.csv", 'w') as outfile:
	writer = csv.writer(outfile)
	for row in ids_and_cats:
		writer.writerow(row)
