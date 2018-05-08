from pyspark import SparkContext
import re
# import glob
import os


def grab_title(document):
    title_pattern = r"\\title\{(.*?)\}"
    document_text = document[1]
    title_check = re.search(title_pattern, document_text, re.MULTILINE | re.DOTALL)
    if title_check != None:
        title_start_index = title_check.start(1)
        document_length = len(document_text)

        running_tally = 1 # started with one forward brace
        i = title_start_index
        while (running_tally > 0):

            if i >= document_length:
                break

            next_char = document_text[i]

            if (next_char == '{'):
                running_tally += 1
            elif (next_char == '}'):
                running_tally -= 1

            i += 1

        title_text = document_text[title_start_index:i-1]
        words = title_text.split()
        for word in words:
            if not word.startswith("\\$"):
                yield (word, 1)
        #return((document[0], title_text))

    #
    # title = False
    #
    # for line in lines:
    #     # line = line.strip()
    #     # print(line)
    #     # input()
    #     if line = "":
    #         continue
    #     else:
    #         title_check = re.match(title_pattern,line)
    #         if title_check != None:
    #
    #             return(title_check.group(1))




sc = SparkContext('local[*]', 'App Name')

in_dir = './outdir3'
data_path = os.path.join(in_dir,'*.tex')
tex_files = sc.wholeTextFiles(data_path)
titles = tex_files.flatMap(grab_title)

for t in titles.take(50):
    print(t)
    print('\n\n')
