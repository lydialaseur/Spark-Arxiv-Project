from pyspark import SparkContext
import re
# import glob
import os

def parse_curly_braces(document_text, start_index, document_length):
    running_tally = 1 # started with one forward brace
    i = start_index

    while (running_tally > 0):

        if i >= document_length:
            break

        next_char = document_text[i]

        if (next_char == '{'):
            running_tally += 1
        elif (next_char == '}'):
            running_tally -= 1

        i += 1

        text = document_text[start_index:i-1]

    return(text)

def grab_text(document, pattern, parse = False):
    document_path, document_text = document
    document_id = document_path.split('/')[-1][5:10]
    text_check = re.findall(pattern, document_text)
    if text_check:

        if parse:
            text_start_index = text_check.start(1)
            document_length = len(document_text)
            text = parse_curly_braces(document_text, text_start_index, document_length)
        else:
            text = text_check

        yield (document_id,text)


sc = SparkContext('local[*]', 'App Name')

in_dir = './outdir3'
data_path = os.path.join(in_dir,'*.tex')
tex_files = sc.wholeTextFiles(data_path)


email_pattern = r"([a-zA-Z0-9-_.]+@[a-zA-Z0-9-_]+?\.[a-zA-Z0-9-_.]+)"

emails = tex_files.flatMap(lambda f: grab_text(f,email_pattern))
print(emails.count())
emails.saveAsTextFile('emails_2')
