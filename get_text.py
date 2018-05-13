from pyspark import SparkContext
import re
# import glob
import os


def grab_text(document, pattern, parse_curly_braces = False):
    document_path, document_text = document
    document_id = document_path.split('/')[-1][5:10]
    text_check = re.search(pattern, document_text, re.MULTILINE | re.DOTALL)
    if text_check:

        if parse_curly_braces:
            text_start_index = text_check.start(1)
            document_length = len(document_text)

            running_tally = 1 # started with one forward brace
            i = text_start_index


            while (running_tally > 0):

                if i >= document_length:
                    break

                next_char = document_text[i]

                if (next_char == '{'):
                    running_tally += 1
                elif (next_char == '}'):
                    running_tally -= 1

                i += 1

            text = document_text[text_start_index:i-1]
        else:
            text = text_check.group(1)

        yield (document_id,text)
        # words = title_text.split()
        # for word in words:
        #     if not word.startswith("\\$"):
        #         yield (word, 1)





sc = SparkContext('local[*]', 'App Name')

in_dir = './outdir3'
data_path = os.path.join(in_dir,'*.tex')
tex_files = sc.wholeTextFiles(data_path)


title_pattern = r"\\title\{(.*?)\}"
titles = tex_files.flatMap(lambda f: grab_text(f,title_pattern,True))
titles.saveAsTextFile('full_titles')



abstract_pattern = r"\\begin\{abstract\}(.*?)\\end\{abstract\}"
abstracts = tex_files.flatMap(lambda f: grab_text(f,abstract_pattern))
abstracts.saveAsTextFile('full_abstracts')
