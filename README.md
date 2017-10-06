# Topic Modeler
The Scandinavian Topic Modeler is a tool developed to topic model English, Danish, Norwegian, and Swedish corpora. The program was developed by Brigham Young University's [Nordic Digital Humanities Lab](https://www.nordicdh.org'). It features a GUI that allows the user to quickly customize and run topic models. Topic models generated through the program produce word clouds for each topic, scatterplots of topic distribution, chunked passages (if applicable), and csv files containing the models' raw data.

# Usage
An OSX version of the Topic Modeler can be downloaded from the [Nordic Digital Humanities Lab website](https://www.nordicdh-beta.org/downloads'). At this time, there are not currently compiled binaries for Windows nor Linux. For use in an IDE, use pip to install the following dependencies: PIL, PyQt5, rippletagger, wordcloud, gensim, nltk, matplotlib. Some of the listed libraries may require additional dependencies.

When the Scandinavian Topic Modeler is first opened a window will appear with several fields. The MALLET Path field takes the file path to the MALLET Unix Executable which can be found in the zip file available [here](http://mallet.cs.umass.edu/dist/mallet-2.0.8.zip). The Input Path field takes the directory path to the folder where your corpus is stored. Your corpus should be comprised entirely of text files and placed in a directory without any additional files. The Output Path field takes the directory path for a folder where you want your results to be stored. The Stop Words field takes the file path to your stop words file. Your stop words file should be a text file with one word per line. The Chunk Size field takes either a number or the word "document". The Topics field takes a number. This number specifies how many topics the program should generate. The Language field will determine the tagger and stemmer used on your corpus, and the parts of speech selected in the Parts of Speech field will determine which parts of speech are included in the topic model.

The program will run without a stop words file and/or without the MALLET Unix Executable. If you choose to run the program without MALLET, it will use gensim instead. It's important to note that the Scandinvian Topic Modeler will not produce all of the output files normally generated when using MALLET if gensim is used instead.

For more information/clarification on the program's usage there is a help button included in the program that provides additional detail.

# License
The Scandinavian Topic Modeler is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version. The Scandinavian Topic Modeler is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. For a copy of the GNU General Public License see [http://www.gnu.org/licenses/](http://www.gnu.org/licenses/).

# Citations
The Scandinavian Topic Modeler is made possible thanks to these pieces of software and their authors. Citations are in the authors' requested formats or in APA if no specific format was requested.

- Dat Quoc Nguyen, Dai Quoc Nguyen, Dang Duc Pham and Son Bao Pham. [RDRPOSTagger: A Ripple Down Rules-based Part-Of-Speech Tagger](http://www.aclweb.org/anthology/E14-2005). In Proceedings of the Demonstrations at the 14th Conference of the European Chapter of the Association for Computational Linguistics, EACL 2014, pp. 17-20, 2014. [\[.PDF\]](http://www.aclweb.org/anthology/E14-2005) [\[.bib\]](http://www.aclweb.org/anthology/E14-2005.bib)

- Dat Quoc Nguyen, Dai Quoc Nguyen, Dang Duc Pham and Son Bao Pham. [A Robust Transformation-Based Learning Approach Using Ripple Down Rules for Part-Of-Speech Tagging](http://content.iospress.com/articles/ai-communications/aic698). AI Communications (AICom), vol. 29, no. 3, pp. 409-422, 2016. [\[.PDF\]](http://arxiv.org/pdf/1412.4021.pdf) [\[.bib\]](http://rdrpostagger.sourceforge.net/AICom.bib)

- Stenstrom, Emil (2016). rippletagger (Version 0.2)\[Computer Software\]. Stockholm, Sweden. Available from [https://github.com/EmilStenstrom/rippletagger](https://github.com/EmilStenstrom/rippletagger)

- Mueller, Andreas (2017). word_cloud (Version 1.2.1)\[Computer Software\]. New York City, NY: Columbia University. Available from [https://github.com/amueller/word_cloud](https://github.com/amueller/word_cloud)

- \[Řehůřek and Sojka(2010)\] R. Řehůřek and P. Sojka. Software Framework for Topic Modelling with Large Corpora. In Proceedings of the LREC 2010 Workshop on New Challenges for NLP Frameworks, pages 45–50, Valletta, Malta, May 2010. ELRA.
[http://is.muni.cz/publication/884893/en](http://is.muni.cz/publication/884893/en).

- McCallum, Andrew Kachites.  "MALLET: A Machine Learning for Language Toolkit." [http://mallet.cs.umass.edu](http://mallet.cs.umass.edu). 2002.
