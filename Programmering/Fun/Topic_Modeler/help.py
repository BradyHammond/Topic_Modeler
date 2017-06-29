"""=================================================="""
"""                  TOPIC MODELER                   """
"""=================================================="""
""" AUTHOR: Brady Hammond                            """
""" CREATED: 12/17/16                                """
""" EDITED BY: Brady Hammond                         """
""" EDITED: 05/26/17                                 """
"""=================================================="""
"""                    FILE SETUP                    """
"""=================================================="""

from PyQt5 import QtCore, QtGui, QtWidgets
import re

"""=================================================="""
"""                CLASS DEFINITIONS                 """
"""=================================================="""

class Ui_help_dialog(object):
    def setupUi(self, help_dialog):
        help_dialog.setObjectName("help_dialog")
        help_dialog.resize(700, 390)
        help_dialog.setFocusPolicy(QtCore.Qt.TabFocus)

        self.help_label = QtWidgets.QLabel(help_dialog)
        self.help_label.setGeometry(QtCore.QRect(20, 20, 350, 20))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.help_label.setFont(font)
        self.help_label.setObjectName("help_label")

        self.search_bar = QtWidgets.QLineEdit(help_dialog)
        self.search_bar.setGeometry(QtCore.QRect(370, 20, 150, 20))
        self.search_bar.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.search_bar.setObjectName("search_bar")
        self.search_bar.returnPressed.connect(self.search)

        self.clear_button = QtWidgets.QPushButton(help_dialog)
        self.clear_button.setGeometry(QtCore.QRect(500, 20, 20, 20))
        font = QtGui.QFont()
        font.setFamily(".SF NS Text")
        self.clear_button.setFont(font)
        self.clear_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.clear_button.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("x_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.clear_button.setIcon(icon)
        self.clear_button.setAutoDefault(False)
        self.clear_button.setFlat(True)
        self.clear_button.setObjectName("clear_button")
        self.clear_button.clicked.connect(self.clearSearch)

        self.search_button = QtWidgets.QPushButton(help_dialog)
        self.search_button.setGeometry(QtCore.QRect(520, 20, 80, 20))
        font = QtGui.QFont()
        font.setKerning(True)
        self.search_button.setFont(font)
        self.search_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.search_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.search_button.setObjectName("search_button")
        self.search_button.clicked.connect(self.search)

        self.quit_button = QtWidgets.QPushButton(help_dialog)
        self.quit_button.setGeometry(QtCore.QRect(600, 20, 80, 20))
        font = QtGui.QFont()
        font.setKerning(True)
        self.quit_button.setFont(font)
        self.quit_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.quit_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.quit_button.setObjectName("quit_button")
        self.quit_button.clicked.connect(help_dialog.close)

        self.help_frame = QtWidgets.QFrame(help_dialog)
        self.help_frame.setGeometry(QtCore.QRect(20, 50, 660, 320))
        self.help_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.help_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.help_frame.setObjectName("help_frame")

        self.help_list_view = QtWidgets.QListView(self.help_frame)
        self.help_list_view.setGeometry(QtCore.QRect(10, 10, 315, 300))
        self.help_list_view.setObjectName("help_list_view")
        self.help_list_view.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.help_list_view.clicked.connect(self.populateTextBrowser)

        self.help_text_browser = QtWidgets.QTextBrowser(self.help_frame)
        self.help_text_browser.setGeometry(QtCore.QRect(335, 10, 315, 300))
        self.help_text_browser.setObjectName("help_text_browser")
        self.help_text_browser.setOpenExternalLinks(True)

        self.help_texts = [
            "<p>The Scandinavian Topic Modeler is a tool developed to topic model Danish, Norwegian, and Swedish" +
            " corpora. The program was developed by Brigham Young University's <a href='https://www.nordicdh.org'>" +
            "Nordic Digital Humanities Lab</a>.</p><p>This program is written in <a href='https://www.python.org/'>" +
            "Python</a>, and is made possible thanks to Emil Stenstrom's" +
            " <a href='https://github.com/EmilStenstrom/rippletagger'>rippletagger</a> library and Andreas Mueller's" +
            " <a href='https://github.com/amueller/word_cloud'>wordcloud</a> library.</p><p<The Scandinavian Topic" +
            " Modeler is free software: you can redistribute it and/or modify it under the terms of the GNU General" +
            " Public License as published by the Free Software Foundation, either version 3 of the License, or any" +
            " later version.</p><p>The Scandinavian Topic Modeler is distributed in the hope that it will be useful," +
            " but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A" +
            " PARTICULAR PURPOSE.  See the GNU General Public License for more details.</p><p>For a copy of the GNU" +
            " General Public License see <a href='http://www.gnu.org/licenses/'>http://www.gnu.org/licenses/</a>.</p>",

            "<p>MALLET is a Java-based package for statistical natural language processing, document classification," +
            " clustering, topic modeling, information extraction, and other machine learning applications to text." +
            "</p><p>MALLET is Open Source Software, and is released under the" +
            " <a href='https://opensource.org/licenses/cpl1.0.php'>Common Public License</a>. You are welcome to use" +
            " the code under the terms of the licence for research or commercial purposes, however please acknowledge" +
            " its use with a citation: <i>McCallum, Andrew Kachites. \"MALLET: A Machine Learning for Language" +
            " Toolkit.\"<br>&nbsp;&nbsp;<a href='http://mallet.cs.umass.edu'>http://mallet.cs.umass.edu</a>. 2002." +
            "</i></p><p>For more information on MALLET, please visit <a href='http://mallet.cs.umass.edu'>" +
            "http://mallet.cs.umass.edu</a>.</p>",

            "<p>The MALLET Path field takes the file path to the MALLET Unix Executable. The MALLET Unix Executable" +
            " can be found in the MALLET zip folder downloaded by clicking" +
            " <a href='http://mallet.cs.umass.edu/dist/mallet-2.0.8.zip'>here</a> or by visiting" +
            " <a href='http://mallet.cs.umass.edu/download.php'>http://mallet.cs.umass.edu/download.php</a>.</p>" +
            "<p>Once you have MALLET downloaded, decompress the folder. Next, open the folder and find the directory" +
            " labelled bin. In the bin folder there is a program called \"mallet\" (without any extensions)." +
            " Copy the path to this file (on macOS right click on the program, hold down the OPTIONS button, and" +
            " select <b> Copy \"mallet\" as Pathname</b>; on Windows hold down the Shift key, then right-click the" +
            " file. In the context menu that appears, find and click <b>Copy as path</b>). Once you have" +
            " the path copied, paste it in the MALLET Path field.</p><p>You can also use the file selection dialog" +
            " to get the MALLET Unix Executable path. To do this, click on the button with the folder icon directly" +
            " adjacent to the MALLET Path field. Navigate to the location of the MALLET Unix Executable. Once" +
            " there, select the file and click open. The file selection dialog will automatically fill the MALLET" +
            " Path field with the correct value.</p>",

            "<p>The Input Path field takes the directory path to the folder where your corpus is stored. Your corpus" +
            " should be comprised entirely of text files and placed in a directory without any additional files.</p>" +
            "<p>Navigate to where your corpus folder is located and copy the path to that folder (on macOS right" +
            " click on the program, hold down the OPTIONS button, and select <b>Copy \"folder\" as Pathname</b>; on" +
            " Windows hold down the Shift key, then right-click the file. In the context menu that appears, find and" +
            " click <b>Copy as path</b>). Once you have the path copied, paste it in the Input Path field.</p><p>You" +
            " can also use the folder selection dialog to get the path to your corpus. To do this, click on the" +
            " button with the folder icon directly adjacent to the Input Path field. Navigate to the location of your" +
            " corpus. Once there, select the folder and click open. The folder selection dialog will automatically" +
            " fill the Input Path field with the correct value.</p>",

            "<p>Your documents should be saved as plain text files (they should have the extension .txt). You do not" +
            " have to do any additional formatting to your corpus. The program will take care of lemmatization," +
            " part of speech tagging, and chunking.</p>",

            "<p>The Output Path field takes the directory path to a folder where your results will be" +
            " stored. This can be any location on your computer.</p><p>Navigate to where you want your results to be"
            " stored (on macOS right click on the program, hold down the OPTIONS button, and select <b>Copy \"folder\""
            " as Pathname</b>; on Windows hold down the Shift key, then right-click the file. In the context menu" +
            " that appears, find and click <b>Copy as path</b>). Once you have the path copied, paste it in the" +
            " Output Path field.</p><p>You can also use the folder selection dialog to get the path for your desired" +
            " results location. To do this, click on the button with the folder icon directly adjacent to the Output" +
            " Path field. Next, navigate to the location of your corpus. Once there, select the folder and click" +
            " open. The folder selection dialog will automatically fill the Output Path field with the correct" +
            " value.</p>",

            "<p>The Stop Words field takes the file path to your stop words file. Your stop words file should be a" +
            " text file﻿(it should have the extension .txt) with one word per line. If your stop words file is not" +
            " formatted properly, the program will still attempt to read your stop words, but may not read them" +
            " correctly.</p><p>Navigate to where your stop words file is located and copy the path to that file (on" +
            " macOS right click on the file, hold down the OPTIONS button, and select <b>Copy \"file\" as" +
            " Pathname</b>; on Windows hold down the Shift key, then right-click the file. In the context menu that" +
            " appears, find and click <b>Copy as path</b>). Once you have the path copied, paste it in the Stop Words" +
            " field.</p><p>You can also use the file selection dialog to get the path to your stop words. To do this," +
            " click on the button with the folder icon directly adjacent to the Stop Words field. Navigate to the" +
            " location of your stop words file. Once there, select the file and click open. The file selection dialog" +
            " will automatically fill the Stop Words field with the correct value.</p><p>It is not necessary to" +
            " give stop words, but stop words do yield better reuslts.</p>",

            "<p>Your stop words should be in a plain text file (it should have the extension .txt) with one word per" +
            " line. Words should <b>NOT</b> have commas after them. Words should only be separated by a carriage" +
            " return (a new line). Comments can be added to your stop words file by starting a line with the \"#\"" +
            " character. The program will ignore any comments in your file.</p><p>If your stop words file is not" +
            " formatted properly, the program will still attempt to read your stop words, but it may not be able to" +
            " read them correctly. An error message will appear if your stop words file is not formatted correctly." +
            " </p>",

            "<p>The Chunk Size field takes either a number or the word \"document\".</p><p>Chunking breaks your" +
            " document into smaller pieces. This allows the model to discover themes that only occur in specific" +
            " places within your documents and not just across documents. Authorities on topic modeling recommend" +
            " using chunks between 500 and 1000 words. The number you enter in the Chunk Size field specifies how" +
            " many words the program should break your documents into before running the topic model. Chunked" +
            " documents are stored in temporary memory, so your saved documents will not be affected by the chunking" +
            " process.</p><p>Sometimes it makes more sense to topic model documents in their entirety (e.g." +
            " periodicals). To skip the chunking process, and topic model complete documents, enter the word" +
            " \"document\" in the Chunk Size field.</p>",

            "<p>The Topics field takes a number. This number specifies how many topics the program should generate." +
            "</p><p>The number of topics you should use will vary based on your corpora. If your number is too small," +
            " your topics will be excessively general. If your number is too large, you will get a number of topics" +
            " that don't make sense. The best way to decide what number to use is by running the program multiple" +
            " times and seeing what number works best.</p>",

            "<p>There are 4 languages supported by the Scandinavian Topic Modeler. These are: English, Danish," +
            " Norwegian (bokmål), and Swedish. The Topic Modeler is restricted to these languages due to the" +
            " availability of part of speech taggers and lemmatizers in different languages. The language you" +
            " choose when running a topic model should correspond to the language of your documents.</p>",

            "<p>The part of speech options are based on the part of speech tags from the Universal Dependencies" +
            " Project. Here are the options and what parts of speech they correspond to:</p><ul><li>ADJ: adjective" +
            "</li><li>ADV: adverb</li><li>INTJ: interjection</li><li>NOUN: noun</li><li>PROPN: proper noun</li><li>" +
            " VERB: verb</li><li>ADP: adposition</li><li>AUX: auxiliary</li><li>CCONJ: coordinating conjunction</li>" +
            "<li>DET: determiner</li><li>NUM: numeral</li><li>PART: particle</li><li>PRON: pronoun</li><li>SCONJ:" +
            " subordinating conjunction</li></ul><p>For more information on the Universal Dependencies Project or" +
            " its associated parts of speech, please visit <a href=\"http://universaldependencies.org/\">" +
            " http://universaldependencies.org/</a>.",

            "<p>Running time will vary depending on the length of your corpus. Shorter corpora will take less time" +
            " to run a topic model, while longer corpora will take more time to run a topic model. On average a full" +
            " length corpus will take 4 to 5 minutes to finish a topic model. The program has been optimized to" +
            " decrease runtime as much as possible.</p>",

            "<p>This program has been extensively tested, and there are error checks in place. Despite this" +
            " programmers are not perfect, and there will inevitably be previously undiscovered bugs in the program." +
            " If you experience one of these bugs, please report it by emailing <a href=\"" +
            "mailto:support@nordicdh-beta.org\">support@nordicdh-beta.org</a>. The more information you can provide" +
            " in your email, the more likely our development team here at BYU's Nordic Digital Humanities Lab will" +
            " be able to fix the problem.</p>",

            "<p>If you have a question that is not answered in this help tab, please email <a href=\"" +
            "mailto:support@nordicdh-beta.org\">support@nordicdh-beta.org</a>. We will try and respond to your" +
            " questions as soon as possible.</p>"
        ]

        self.help_options = [
            "What is the Scandinavian Topic Modeler?",
            "What is MALLET?",
            "What should I put in the MALLET Path field?",
            "What should I put in the Input Path field?",
            "How should I format my documents?",
            "What should I put in the Output Path field?",
            "What should I put in the Stop Words field?",
            "How should my stop words be formatted?",
            "What should I put in the Chunk Size field?",
            "What should I put in the Topics field?",
            "What language options are there?",
            "What are the Part of Speech options?",
            "How long does running a topic model take?",
            "The program closed unexpectedly, what should I do?",
            "I have other questions, what should I do?"
        ]

        self.populateList()
        self.retranslateUi(help_dialog)
        QtCore.QMetaObject.connectSlotsByName(help_dialog)

    # ==================================================

    def retranslateUi(self, help_dialog):
        _translate = QtCore.QCoreApplication.translate
        help_dialog.setWindowTitle(_translate("help_dialog", "Help"))
        self.help_label.setText(_translate("help_dialog", "Scandinavian Topic Modeler Help"))
        self.search_bar.setPlaceholderText(_translate("help_dialog", "Search..."))
        self.search_button.setText(_translate("help_dialog", "Search"))
        self.quit_button.setText(_translate("help_dialog", "Quit"))

    # ==================================================

    def populateList(self):
        model = QtGui.QStandardItemModel()

        for option in self.help_options:
            item = QtGui.QStandardItem(option)
            model.appendRow(item)

        self.help_list_view.setModel(model)

    # ==================================================

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def populateTextBrowser(self):
        index = self.help_list_view.selectedIndexes()

        self.help_text_browser.setText(self.help_texts[index[0].row()])

    # ==================================================

    def clearSearch(self):
        self.search_bar.setText("")

    def search(self):
        results = [text for text in self.help_texts if self.search_bar.text().lower() in text.lower()]

        if len(results) > 0:
            indices = []
            for result in results:
                indices.append(self.help_texts.index(result))

            regex_string = "(^|\s)"
            for letter in self.search_bar.text().lower():
                regex_string = regex_string + "[" + letter + "|" + letter.upper() + "]"

            search_result = ""
            for index in indices:
                paragraph_list = self.help_texts[index].split("</p>")
                for paragraph in paragraph_list:
                    paragraph = re.sub("<p>", "", paragraph)
                    individual_search_entry = "<i>" + self.help_options[index][:-1] + ":</i> "
                    if self.search_bar.text().lower() in paragraph.lower():
                        match = re.search(regex_string, paragraph)

                        if match is None:
                            highlighted_word = self.search_bar.text().lower()
                        else:
                            highlighted_word = "<span style=\"background-color: #FFFF00\">" + match.group(0) + "</span>"

                        individual_search_entry = individual_search_entry + re.sub(regex_string, highlighted_word, paragraph)
                        search_result = search_result + "<p>" + individual_search_entry + "</p>"

            self.help_text_browser.setText(search_result)
        else:
            self.help_text_browser.setText("<p>No Results Found</p>")


"""=================================================="""
"""                       EOF                        """
"""=================================================="""