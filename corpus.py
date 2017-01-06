"""=================================================="""
"""                      CORPUS                      """
"""=================================================="""
""" AUTHOR: Brady Hammond                            """
""" CREATED: 12/17/16                                """
""" EDITED BY: -----                                 """
""" EDITED: --/--/--                                 """
"""=================================================="""
"""                    FILE SETUP                    """
"""=================================================="""

from gensim import corpora, utils
import os

"""=================================================="""
"""                CLASS DEFINITIONS                 """
"""=================================================="""

class corpusObject(object):

    def __init__(self, directory):
        self.directory = directory
        self.dictionary = corpora.Dictionary(self.iterateDocuments(directory))
        self.dictionary.filter_extremes()

    def __iter__(self):
        for tokens in self.iterateDocuments(self.directory):
            yield self.dictionary.doc2bow(tokens)

    def iterateDocuments(self, directory):
        for file_name in os.listdir(directory):
            document = open(os.path.join(directory, file_name), encoding="utf-8", errors="ignore").read()
            yield utils.simple_preprocess(document)

"""=================================================="""
"""                       EOF                        """
"""=================================================="""