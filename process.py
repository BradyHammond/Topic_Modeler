"""=================================================="""
"""                      FORMAT                      """
"""=================================================="""
""" AUTHOR: Brady Hammond                            """
""" CREATED: 09/26/17                                """
""" EDITED BY: -----                                 """
""" EDITED: --/--/--                                 """
"""=================================================="""
"""                    FILE SETUP                    """
"""=================================================="""

import datetime
import io
import logging
import os
import re
import string
from nltk.stem.snowball import SnowballStemmer
from rippletagger.tagger import Tagger

"""=================================================="""
"""                CLASS DEFINITIONS                 """
"""=================================================="""

class fileProcessor(object):
    def __init__(self, language, chunk_size, passages_directory, temporary_directory, parts_of_speech, stop_words):
        self.language = language
        self.chunk_size = chunk_size
        self.passages_directory = passages_directory
        self.temporary_directory = temporary_directory
        self.parts_of_speech = parts_of_speech
        self.stop_words = stop_words

    # ==================================================

    def chunkCorpus(self, corpus, number):
        for i in range(0, len(corpus), number):
                yield corpus[i:i + number]

    # ==================================================

    def processFile(self, subdirectory, file):
        if not file.startswith('.'):
            file_name = os.path.splitext(file)[0]
            print(str(datetime.datetime.now())[:-3] + " : INFO : processing " + file_name)
            logging.info("starting file processor")
            file_path = os.path.join(subdirectory, file)

            working_file = io.open(file_path, encoding="utf-8", errors="ignore")
            working_file_text = working_file.read()
            working_file_text = working_file_text.lower().rstrip("/n")

            if self.language == "Danish":
                stemmer = SnowballStemmer("danish")
                tagger = Tagger(language="da")

            elif self.language == "Norwegian":
                stemmer = SnowballStemmer("norwegian")
                tagger = Tagger(language="no")

            elif self.language == "Swedish":
                stemmer = SnowballStemmer("swedish")
                tagger = Tagger(language="sv-2")

            else:
                stemmer = SnowballStemmer("english")
                tagger = Tagger(language="en-1")

            tagged_text = tagger.tag(working_file_text)
            if self.chunk_size.isalpha():

                chunked_file = io.open(self.temporary_directory + "/" + file_name + ".txt", "w", encoding="utf-8")
                for tag in tagged_text:
                    if tag[1] in self.parts_of_speech:
                        word = re.sub("»|«", "", tag[0])
                        word = word.strip(string.punctuation)
                        stemmed_tag = stemmer.stem(word)
                        if stemmed_tag in self.stop_words:
                            pass
                        else:
                            chunked_file.write(stemmed_tag + " ")
                chunked_file.close()

            else:
                chunks = list(self.chunkCorpus(tagged_text, int(self.chunk_size)))

                chunk_number = 1
                for chunk in chunks:
                    if len(str(chunk_number)) == 1:
                        chunked_file = io.open(self.passages_directory + "/" + file_name + "_000" + str(chunk_number) +
                                               ".txt", "w", encoding="utf-8")
                    elif len(str(chunk_number)) == 2:
                        chunked_file = io.open(self.passages_directory + "/" + file_name + "_00" + str(chunk_number) +
                                               ".txt", "w", encoding="utf-8")
                    elif len(str(chunk_number)) == 3:
                        chunked_file = io.open(self.passages_directory + "/" + file_name + "_0" + str(chunk_number) +
                                               ".txt", "w", encoding="utf-8")
                    else:
                        chunked_file = io.open(self.passages_directory + "/" + file_name + "_" + str(chunk_number) +
                                               ".txt", "w", encoding="utf-8")
                    for tag in chunk:
                        chunked_file.write(tag[0] + " ")
                    chunked_file.close()

                    if len(str(chunk_number)) == 1:
                        chunked_file = io.open(self.temporary_directory + "/" + file_name + "_000" + str(chunk_number) +
                                               ".txt", "w", encoding="utf-8")
                    elif len(str(chunk_number)) == 2:
                        chunked_file = io.open(self.temporary_directory + "/" + file_name + "_00" + str(chunk_number) +
                                               ".txt", "w", encoding="utf-8")
                    elif len(str(chunk_number)) == 3:
                        chunked_file = io.open(self.temporary_directory + "/" + file_name + "_0" + str(chunk_number) +
                                               ".txt", "w", encoding="utf-8")
                    else:
                        chunked_file = io.open(self.temporary_directory + "/" + file_name + "_" + str(chunk_number) +
                                               ".txt", "w", encoding="utf-8")

                    for tag in chunk:
                        if tag[1] in self.parts_of_speech:
                            word = re.sub("»|«", "", tag[0])
                            word = word.strip(string.punctuation)
                            stemmed_tag = stemmer.stem(word)
                            if stemmed_tag in self.stop_words:
                                pass
                            else:
                                chunked_file.write(stemmed_tag + " ")
                    chunked_file.close()
                    chunk_number += 1

"""=================================================="""
"""                       EOF                        """
"""=================================================="""
