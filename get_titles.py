from pyspark import SparkContext
import re
import os


def grab_title(document):
    title_pattern = r"\\title\{(.*?)\}"
    document_path, document_text = document
    document_id = document_path.split('/')[-1][5:10]
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
            banned_characters = set("\\$=}{+")
            if not any((c in banned_characters) for c in word):
                word = word.lower()
                pattern = re.escape('?!.%')
                word = re.sub('[{0}]'.format(pattern), '', word)
                yield (word, 1)


sc = SparkContext('local[*]', 'App Name')

in_dir = './outdir3'
data_path = os.path.join(in_dir,'*.tex')
tex_files = sc.wholeTextFiles(data_path)
title_words = tex_files.flatMap(grab_title)
title_word_counts = title_words.reduceByKey(lambda x,y : x + y)
title_word_counts.saveAsTextFile('title_word_counts_3')
