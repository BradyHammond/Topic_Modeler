"""=================================================="""
"""                  TOPIC MODELER                   """
"""=================================================="""
""" AUTHOR: Brady Hammond                            """
""" CREATED: 12/17/16                                """
""" EDITED BY: -----                                 """
""" EDITED: --/--/--                                 """
"""=================================================="""
"""                    FILE SETUP                    """
"""=================================================="""

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QApplication
from gensim.models.wrappers import ldamallet
from rippletagger.tagger import Tagger
from nltk.stem.snowball import SnowballStemmer
from multiprocessing import Pool
from corpus import corpusObject
import json
import sys
import os
import logging
import string
import shutil
import datetime

"""=================================================="""
"""                CLASS DEFINITIONS                 """
"""=================================================="""


class Ui_main_window(object):
    def setupUi(self, main_window):
        main_window.setObjectName("main_window")
        main_window.setWindowModality(QtCore.Qt.WindowModal)
        main_window.resize(700, 360)
        main_window.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        main_window.setInputMethodHints(QtCore.Qt.ImhNone)

        self.grid_layout_widget_I = QtWidgets.QWidget(main_window)
        self.grid_layout_widget_I.setGeometry(QtCore.QRect(0, 0, 681, 351))
        self.grid_layout_widget_I.setObjectName("grid_layout_widget_I")

        self.grid_layout_main = QtWidgets.QGridLayout(self.grid_layout_widget_I)
        self.grid_layout_main.setContentsMargins(0, 0, 0, 0)
        self.grid_layout_main.setObjectName("grid_layout_main")

        self.byu_humanities_logo = QtWidgets.QLabel(self.grid_layout_widget_I)
        self.byu_humanities_logo.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.byu_humanities_logo.setPixmap(QtGui.QPixmap("images/logo.png"))
        self.byu_humanities_logo.setAlignment(QtCore.Qt.AlignCenter)
        self.byu_humanities_logo.setObjectName("byu_humanities_logo")
        self.grid_layout_main.addWidget(self.byu_humanities_logo, 0, 0, 1, 1)

        self.quit_button = QtWidgets.QPushButton(self.grid_layout_widget_I)
        self.quit_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.quit_button.setObjectName("quit_button")
        self.quit_button.clicked.connect(main_window.close)
        self.grid_layout_main.addWidget(self.quit_button, 1, 4, 1, 1)

        self.parameters_box = QtWidgets.QGroupBox(self.grid_layout_widget_I)
        self.parameters_box.setTitle("")
        self.parameters_box.setAlignment(QtCore.Qt.AlignCenter)
        self.parameters_box.setObjectName("parameters_box")
        self.grid_layout_widget_II = QtWidgets.QWidget(self.parameters_box)

        self.grid_layout_widget_II.setGeometry(QtCore.QRect(10, 20, 341, 281))
        self.grid_layout_widget_II.setObjectName("grid_layout_widget_II")
        self.sub_grid_layout_I = QtWidgets.QGridLayout(self.grid_layout_widget_II)
        self.sub_grid_layout_I.setContentsMargins(0, 0, 0, 0)
        self.sub_grid_layout_I.setObjectName("sub_grid_layout_I")

        self.chunk_size_label = QtWidgets.QLabel(self.grid_layout_widget_II)
        self.chunk_size_label.setObjectName("chunk_size_label")
        self.sub_grid_layout_I.addWidget(self.chunk_size_label, 4, 0, 1, 1)

        self.mallet_path_input = QtWidgets.QLineEdit(self.grid_layout_widget_II)
        self.mallet_path_input.setObjectName("mallet_path_input")
        self.sub_grid_layout_I.addWidget(self.mallet_path_input, 0, 1, 1, 1)

        self.input_file_selector = QtWidgets.QToolButton(self.grid_layout_widget_II)
        self.input_file_selector.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/file.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.input_file_selector.setIcon(icon)
        self.input_file_selector.setObjectName("input_file_selector")
        self.input_file_selector.clicked.connect(self.selectInputPath)
        self.sub_grid_layout_I.addWidget(self.input_file_selector, 1, 2, 1, 1)

        self.input_path_label = QtWidgets.QLabel(self.grid_layout_widget_II)
        self.input_path_label.setObjectName("input_path_label")
        self.sub_grid_layout_I.addWidget(self.input_path_label, 1, 0, 1, 1)

        self.topics_label = QtWidgets.QLabel(self.grid_layout_widget_II)
        self.topics_label.setObjectName("topics_label")
        self.sub_grid_layout_I.addWidget(self.topics_label, 5, 0, 1, 1)

        self.language_input = QtWidgets.QComboBox(self.grid_layout_widget_II)
        self.language_input.setObjectName("language_input")
        self.language_input.addItems(["English", "Danish", "Norwegian", "Swedish"])
        self.sub_grid_layout_I.addWidget(self.language_input, 6, 1, 1, 1)

        self.stop_words_label = QtWidgets.QLabel(self.grid_layout_widget_II)
        self.stop_words_label.setObjectName("stop_words_label")
        self.sub_grid_layout_I.addWidget(self.stop_words_label, 3, 0, 1, 1)

        self.output_path_label = QtWidgets.QLabel(self.grid_layout_widget_II)
        self.output_path_label.setObjectName("output_path_label")
        self.sub_grid_layout_I.addWidget(self.output_path_label, 2, 0, 1, 1)

        self.output_path_input = QtWidgets.QLineEdit(self.grid_layout_widget_II)
        self.output_path_input.setObjectName("output_path_input")
        self.sub_grid_layout_I.addWidget(self.output_path_input, 2, 1, 1, 1)

        self.stop_words_file_selector = QtWidgets.QToolButton(self.grid_layout_widget_II)
        self.stop_words_file_selector.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.stop_words_file_selector.setIcon(icon)
        self.stop_words_file_selector.setObjectName("stop_words_file_selector")
        self.stop_words_file_selector.clicked.connect(self.selectStopWordsPath)
        self.sub_grid_layout_I.addWidget(self.stop_words_file_selector, 3, 2, 1, 1)

        self.language_label = QtWidgets.QLabel(self.grid_layout_widget_II)
        self.language_label.setObjectName("language_label")
        self.sub_grid_layout_I.addWidget(self.language_label, 6, 0, 1, 1)

        self.input_path_input = QtWidgets.QLineEdit(self.grid_layout_widget_II)
        self.input_path_input.setObjectName("input_path_input")
        self.sub_grid_layout_I.addWidget(self.input_path_input, 1, 1, 1, 1)

        self.mallet_file_selector = QtWidgets.QToolButton(self.grid_layout_widget_II)
        self.mallet_file_selector.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.mallet_file_selector.setIcon(icon)
        self.mallet_file_selector.setObjectName("mallet_file_selector")
        self.mallet_file_selector.clicked.connect(self.selectMalletPath)
        self.sub_grid_layout_I.addWidget(self.mallet_file_selector, 0, 2, 1, 1)

        self.mallet_path_label = QtWidgets.QLabel(self.grid_layout_widget_II)
        self.mallet_path_label.setObjectName("mallet_path_label")
        self.sub_grid_layout_I.addWidget(self.mallet_path_label, 0, 0, 1, 1)

        self.output_file_selector = QtWidgets.QToolButton(self.grid_layout_widget_II)
        self.output_file_selector.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.output_file_selector.setIcon(icon)
        self.output_file_selector.setObjectName("output_file_selector")
        self.output_file_selector.clicked.connect(self.selectOutputPath)
        self.sub_grid_layout_I.addWidget(self.output_file_selector, 2, 2, 1, 1)

        self.stop_words_input = QtWidgets.QLineEdit(self.grid_layout_widget_II)
        self.stop_words_input.setObjectName("stop_words_input")
        self.sub_grid_layout_I.addWidget(self.stop_words_input, 3, 1, 1, 1)

        self.chunk_size_input = QtWidgets.QLineEdit(self.grid_layout_widget_II)
        self.chunk_size_input.setObjectName("chunk_size_input")
        self.sub_grid_layout_I.addWidget(self.chunk_size_input, 4, 1, 1, 1)

        self.topics_input = QtWidgets.QLineEdit(self.grid_layout_widget_II)
        self.topics_input.setObjectName("topics_input")
        self.sub_grid_layout_I.addWidget(self.topics_input, 5, 1, 1, 1)

        self.grid_layout_widget_III = QtWidgets.QWidget(self.parameters_box)
        self.grid_layout_widget_III.setGeometry(QtCore.QRect(360, 30, 191, 273))
        self.grid_layout_widget_III.setObjectName("gridLayoutWidget_3")
        self.sub_grid_layout_II = QtWidgets.QGridLayout(self.grid_layout_widget_III)
        self.sub_grid_layout_II.setContentsMargins(0, 0, 0, 0)
        self.sub_grid_layout_II.setObjectName("sub_grid_layout_II")

        self.punct_checkbox = QtWidgets.QCheckBox(self.grid_layout_widget_III)
        self.punct_checkbox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.punct_checkbox.setObjectName("punct_checkbox")
        self.sub_grid_layout_II.addWidget(self.punct_checkbox, 6, 2, 1, 1)

        self.sconj_checkbox = QtWidgets.QCheckBox(self.grid_layout_widget_III)
        self.sconj_checkbox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.sconj_checkbox.setObjectName("sconj_checkbox")
        self.sub_grid_layout_II.addWidget(self.sconj_checkbox, 5, 2, 1, 1)

        self.pron_checkbox = QtWidgets.QCheckBox(self.grid_layout_widget_III)
        self.pron_checkbox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pron_checkbox.setObjectName("pron_checkbox")
        self.sub_grid_layout_II.addWidget(self.pron_checkbox, 4, 2, 1, 1)

        self.num_checkbox = QtWidgets.QCheckBox(self.grid_layout_widget_III)
        self.num_checkbox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.num_checkbox.setObjectName("num_checkbox")
        self.sub_grid_layout_II.addWidget(self.num_checkbox, 2, 2, 1, 1)

        self.cconj_checkbox = QtWidgets.QCheckBox(self.grid_layout_widget_III)
        self.cconj_checkbox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.cconj_checkbox.setObjectName("cconj_checkbox")
        self.sub_grid_layout_II.addWidget(self.cconj_checkbox, 9, 1, 1, 1)

        self.adj_checkbox = QtWidgets.QCheckBox(self.grid_layout_widget_III)
        self.adj_checkbox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.adj_checkbox.setObjectName("adj_checkbox")
        self.sub_grid_layout_II.addWidget(self.adj_checkbox, 1, 1, 1, 1)

        self.adv_checkbox = QtWidgets.QCheckBox(self.grid_layout_widget_III)
        self.adv_checkbox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.adv_checkbox.setObjectName("adv_checkbox")
        self.sub_grid_layout_II.addWidget(self.adv_checkbox, 2, 1, 1, 1)

        self.det_checkbox = QtWidgets.QCheckBox(self.grid_layout_widget_III)
        self.det_checkbox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.det_checkbox.setObjectName("det_checkbox")
        self.sub_grid_layout_II.addWidget(self.det_checkbox, 1, 2, 1, 1)

        self.sym_checkbox = QtWidgets.QCheckBox(self.grid_layout_widget_III)
        self.sym_checkbox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.sym_checkbox.setObjectName("sym_checkbox")
        self.sub_grid_layout_II.addWidget(self.sym_checkbox, 7, 2, 1, 1)

        self.aux_checkbox = QtWidgets.QCheckBox(self.grid_layout_widget_III)
        self.aux_checkbox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.aux_checkbox.setObjectName("aux_checkbox")
        self.sub_grid_layout_II.addWidget(self.aux_checkbox, 8, 1, 1, 1)

        self.propn_checkbox = QtWidgets.QCheckBox(self.grid_layout_widget_III)
        self.propn_checkbox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.propn_checkbox.setObjectName("propn_checkbox")
        self.sub_grid_layout_II.addWidget(self.propn_checkbox, 5, 1, 1, 1)

        self.part_checkbox = QtWidgets.QCheckBox(self.grid_layout_widget_III)
        self.part_checkbox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.part_checkbox.setObjectName("part_checkbox")
        self.sub_grid_layout_II.addWidget(self.part_checkbox, 3, 2, 1, 1)

        self.x_checkbox = QtWidgets.QCheckBox(self.grid_layout_widget_III)
        self.x_checkbox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.x_checkbox.setObjectName("x_checkbox")
        self.sub_grid_layout_II.addWidget(self.x_checkbox, 8, 2, 1, 1)

        spacer_item = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.sub_grid_layout_II.addItem(spacer_item, 9, 0, 1, 1)

        self.intj_checkbox = QtWidgets.QCheckBox(self.grid_layout_widget_III)
        self.intj_checkbox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.intj_checkbox.setObjectName("intj_checkbox")
        self.sub_grid_layout_II.addWidget(self.intj_checkbox, 3, 1, 1, 1)

        self.verb_checkbox = QtWidgets.QCheckBox(self.grid_layout_widget_III)
        self.verb_checkbox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.verb_checkbox.setObjectName("verb_checkbox")
        self.sub_grid_layout_II.addWidget(self.verb_checkbox, 6, 1, 1, 1)

        self.part_of_speech_label = QtWidgets.QLabel(self.grid_layout_widget_III)
        self.part_of_speech_label.setAlignment(QtCore.Qt.AlignCenter)
        self.part_of_speech_label.setObjectName("part_of_speech_label")
        self.sub_grid_layout_II.addWidget(self.part_of_speech_label, 0, 1, 1, 2)

        self.noun_checkbox = QtWidgets.QCheckBox(self.grid_layout_widget_III)
        self.noun_checkbox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.noun_checkbox.setObjectName("noun_checkbox")
        self.sub_grid_layout_II.addWidget(self.noun_checkbox, 4, 1, 1, 1)

        self.adp_checkbox = QtWidgets.QCheckBox(self.grid_layout_widget_III)
        self.adp_checkbox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.adp_checkbox.setObjectName("adp_checkbox")
        self.sub_grid_layout_II.addWidget(self.adp_checkbox, 7, 1, 1, 1)

        spacer_item_II = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.sub_grid_layout_II.addItem(spacer_item_II, 10, 0, 1, 1)

        self.help_button = QtWidgets.QPushButton(self.grid_layout_widget_III)
        self.help_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.help_button.setObjectName("help_button")
        self.sub_grid_layout_II.addWidget(self.help_button, 10, 1, 1, 2)
        self.grid_layout_main.addWidget(self.parameters_box, 0, 1, 1, 6)

        self.run_model_button = QtWidgets.QPushButton(self.grid_layout_widget_I)
        self.run_model_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.run_model_button.setObjectName("run_model_button")
        self.run_model_button.clicked.connect(self.runModel)
        self.grid_layout_main.addWidget(self.run_model_button, 1, 2, 1, 1)

        self.version_label = QtWidgets.QLabel(self.grid_layout_widget_I)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.version_label.setFont(font)
        self.version_label.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)
        self.version_label.setObjectName("label")
        self.grid_layout_main.addWidget(self.version_label, 1, 6, 1, 1)

        self.run_model_with_sql_button = QtWidgets.QPushButton(self.grid_layout_widget_I)
        self.run_model_with_sql_button.setObjectName("run_model_with_sql_button")
        self.grid_layout_main.addWidget(self.run_model_with_sql_button, 1, 3, 1, 1)

        self.parts_of_speech = []
        self.stop_words = []
        self.temporary_directory = ""
        self.passages_directory = ""
        self.word_clouds_directory = ""
        self.scatter_plot_directory = ""
        self.temporary_directory_error = False
        self.stop_words_formatted_correctly = True

        self.retranslateUi(main_window)
        self.setCheckboxes()
        self.setLanguage()
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslateUi(self, main_window):
        _translate = QtCore.QCoreApplication.translate

        main_window.setWindowTitle(_translate("main_window", "Scandinavian Topic Modeler"))
        self.run_model_button.setText(_translate("main_window", "Run Model"))
        self.quit_button.setText(_translate("main_window", "Quit"))
        self.chunk_size_label.setText(_translate("main_window", "Chunk Size:"))
        self.input_file_selector.setText(_translate("main_window", "..."))
        self.input_path_label.setText(_translate("main_window", "Input Path:"))
        self.topics_label.setText(_translate("main_window", "Topics:"))
        self.stop_words_label.setText(_translate("main_window", "Stop Words:"))
        self.output_path_label.setText(_translate("main_window", "Output Path:"))
        self.stop_words_file_selector.setText(_translate("main_window", "..."))
        self.language_label.setText(_translate("main_window", "Language:"))
        self.mallet_path_label.setText(_translate("main_window", "MALLET Path:"))
        self.output_file_selector.setText(_translate("main_window", "..."))
        self.punct_checkbox.setText(_translate("main_window", "PUNCT"))
        self.sconj_checkbox.setText(_translate("main_window", "SCONJ"))
        self.pron_checkbox.setText(_translate("main_window", "PRON"))
        self.num_checkbox.setText(_translate("main_window", "NUM"))
        self.cconj_checkbox.setText(_translate("main_window", "CCONJ"))
        self.adj_checkbox.setText(_translate("main_window", "ADJ"))
        self.adv_checkbox.setText(_translate("main_window", "ADV"))
        self.det_checkbox.setText(_translate("main_window", "DET"))
        self.sym_checkbox.setText(_translate("main_window", "SYM"))
        self.aux_checkbox.setText(_translate("main_window", "AUX"))
        self.propn_checkbox.setText(_translate("main_window", "PROPN"))
        self.part_checkbox.setText(_translate("main_window", "PART"))
        self.x_checkbox.setText(_translate("main_window", "X"))
        self.intj_checkbox.setText(_translate("main_window", "INTJ"))
        self.verb_checkbox.setText(_translate("main_window", "VERB"))
        self.part_of_speech_label.setText(_translate("main_window", "Parts of Speech:"))
        self.noun_checkbox.setText(_translate("main_window", "NOUN"))
        self.adp_checkbox.setText(_translate("main_window", "ADP"))
        self.help_button.setText(_translate("main_window", "Help"))
        self.version_label.setText(_translate("main_window", "Version 1.0.3"))
        self.run_model_with_sql_button.setText(_translate("main_window", "Run with SQL"))

        preference_data_file = open("files/preference_data.json", "r")
        preference_data = json.load(preference_data_file)
        self.mallet_path_input.setText(_translate("main_window", preference_data["mallet_path"]))
        self.input_path_input.setText(_translate("main_window", preference_data["input_path"]))
        self.output_path_input.setText(_translate("main_window", preference_data["output_path"]))
        self.stop_words_input.setText(_translate("main_window", preference_data["stop_words_path"]))
        self.chunk_size_input.setText(_translate("main_window", preference_data["chunk_size"]))
        self.topics_input.setText(_translate("main_window", preference_data["topics"]))
        preference_data_file.close()

    def setCheckboxes(self):
        preference_data_file = open("files/preference_data.json", "r")
        preference_data = json.load(preference_data_file)

        if "ADJ" in preference_data["parts_of_speech"]:
            self.adj_checkbox.setChecked(True)
        if "ADV" in preference_data["parts_of_speech"]:
            self.adv_checkbox.setChecked(True)
        if "INTJ" in preference_data["parts_of_speech"]:
            self.intj_checkbox.setChecked(True)
        if "NOUN" in preference_data["parts_of_speech"]:
            self.noun_checkbox.setChecked(True)
        if "PROPN" in preference_data["parts_of_speech"]:
            self.propn_checkbox.setChecked(True)
        if "VERB" in preference_data["parts_of_speech"]:
            self.verb_checkbox.setChecked(True)
        if "ADP" in preference_data["parts_of_speech"]:
            self.adp_checkbox.setChecked(True)
        if "AUX" in preference_data["parts_of_speech"]:
            self.aux_checkbox.setChecked(True)
        if "CCONJ" in preference_data["parts_of_speech"]:
            self.cconj_checkbox.setChecked(True)
        if "DET" in preference_data["parts_of_speech"]:
            self.det_checkbox.setChecked(True)
        if "NUM" in preference_data["parts_of_speech"]:
            self.num_checkbox.setChecked(True)
        if "PART" in preference_data["parts_of_speech"]:
            self.part_checkbox.setChecked(True)
        if "PRON" in preference_data["parts_of_speech"]:
            self.pron_checkbox.setChecked(True)
        if "SCONJ" in preference_data["parts_of_speech"]:
            self.sconj_checkbox.setChecked(True)
        if "PUNCT" in preference_data["parts_of_speech"]:
            self.punct_checkbox.setChecked(True)
        if "SYM" in preference_data["parts_of_speech"]:
            self.sym_checkbox.setChecked(True)
        if "X" in preference_data["parts_of_speech"]:
            self.x_checkbox.setChecked(True)

        preference_data_file.close()

    def setLanguage(self):
        preference_data_file = open("files/preference_data.json", "r")

        preference_data = json.load(preference_data_file)
        self.language_input.setCurrentIndex(int(preference_data["language_index"]))
        preference_data_file.close()

    def runModel(self):
        start_time = datetime.datetime.now()
        print("Commencing program: " + str(start_time))
        print("Checking input fields: " + str(datetime.datetime.now() - start_time))
        if self.mallet_path_input.text() == "":
            message_box = QMessageBox()
            message_box.setIcon(QMessageBox.Warning)
            message_box.setWindowTitle("Invalid Parameters")
            message_box.setText("The MALLET path field is currently empty. Please enter a valid path to MALLET.")
            message_box.exec_()

            self.mallet_path_input.setFocus()
            return

        elif not (os.path.isfile(self.mallet_path_input.text()) and os.access(self.mallet_path_input.text(), os.X_OK)):
            message_box = QMessageBox()
            message_box.setIcon(QMessageBox.Warning)
            message_box.setWindowTitle("Invalid Parameters")
            message_box.setText("The MALLET path doesn't seem quite right. Please enter a valid path to MALLET.")
            message_box.exec_()

            self.mallet_path_input.setFocus()
            return

        if self.input_path_input.text() == "":
            message_box = QMessageBox()
            message_box.setIcon(QMessageBox.Warning)
            message_box.setWindowTitle("Invalid Parameters")
            message_box.setText("The input path field is currently empty. Please enter a valid input folder.")
            message_box.exec_()

            self.input_path_input.setFocus()
            return

        elif not os.path.isdir(self.input_path_input.text()):
            message_box = QMessageBox()
            message_box.setIcon(QMessageBox.Warning)
            message_box.setWindowTitle("Invalid Parameters")
            message_box.setText("The input path doesn't seem quite right. Please enter a valid input folder.")
            message_box.exec_()

            self.input_path_input.setFocus()
            return

        text_files = []
        for file in os.listdir(self.input_path_input.text()):
            if file.endswith(".txt"):
                text_files.append(file)

        if len(text_files) < 1:
            message_box = QMessageBox()
            message_box.setIcon(QMessageBox.Warning)
            message_box.setWindowTitle("Invalid Parameters")
            message_box.setText("There don't seem to be any documents in the input folder. Please enter a valid input" +
                                " folder.")
            message_box.exec_()

            self.input_path_input.setFocus()
            return

        if self.output_path_input.text() == "":
            message_box = QMessageBox()
            message_box.setIcon(QMessageBox.Warning)
            message_box.setWindowTitle("Invalid Parameters")
            message_box.setText("The output path field is currently empty. Please enter a valid path output folder.")
            message_box.exec_()

            self.output_path_input.setFocus()
            return

        elif not os.path.isdir(self.output_path_input.text()):
            message_box = QMessageBox()
            message_box.setIcon(QMessageBox.Warning)
            message_box.setWindowTitle("Invalid Parameters")
            message_box.setText("The output path doesn't seem quite right. Please enter a valid output folder.")
            message_box.exec_()

            self.output_path_input.setFocus()
            return

        else:
           if self.output_path_input.text().endswith("/"):
               self.output_path_input.setText(self.output_path_input.text()[:-1])

        if self.stop_words_input.text() != "" and os.path.exists(self.stop_words_input.text()) == False:
            message_box = QMessageBox()
            message_box.setIcon(QMessageBox.Warning)
            message_box.setWindowTitle("Invalid Parameters")
            message_box.setText("The stop words file doesn't seem quite right. Please enter a valid stop words file.")
            message_box.exec_()

            self.stop_words_input.setFocus()
            return

        elif not self.stop_words_input.text().endswith(".txt") and self.stop_words_input.text() != "":
            message_box = QMessageBox()
            message_box.setIcon(QMessageBox.Warning)
            message_box.setWindowTitle("Invalid Parameters")
            message_box.setText("The stop words file doesn't seem quite right. Please enter a valid stop words file.")
            message_box.exec_()

            self.stop_words_input.setFocus()
            return

        if self.chunk_size_input.text() == "":
            message_box = QMessageBox()
            message_box.setIcon(QMessageBox.Warning)
            message_box.setWindowTitle("Invalid Parameters")
            message_box.setText("The chunk size field is currently empty. Please enter a valid chunk size.")
            message_box.exec_()

            self.chunk_size_input.setFocus()
            return

        elif not self.chunk_size_input.text().isdigit():
            message_box = QMessageBox()
            message_box.setIcon(QMessageBox.Warning)
            message_box.setWindowTitle("Invalid Parameters")
            message_box.setText("The chunk size field doesn't seem quite right. Please remember that chunk size" +
                                " should be a number.")
            message_box.exec_()

            self.chunk_size_input.setFocus()
            return

        if self.topics_input.text() == "":
            message_box = QMessageBox()
            message_box.setIcon(QMessageBox.Warning)
            message_box.setWindowTitle("Invalid Parameters")
            message_box.setText("The topics field is currently empty. Please enter a valid number of topics.")
            message_box.exec_()

            self.topics_input.setFocus()
            return

        elif not self.topics_input.text().isdigit():
            message_box = QMessageBox()
            message_box.setIcon(QMessageBox.Warning)
            message_box.setWindowTitle("Invalid Parameters")
            message_box.setText("The topics field doesn't seem quite right. Please remember that topics should be" +
                                " a number.")
            message_box.exec_()

            self.topics_input.setFocus()
            return

        if (self.adj_checkbox.isChecked() == False and self.adv_checkbox.isChecked() == False
            and self.intj_checkbox.isChecked() == False and self.noun_checkbox.isChecked() == False
            and self.propn_checkbox.isChecked() == False and self.verb_checkbox.isChecked() == False
            and self.adp_checkbox.isChecked() == False and self.aux_checkbox.isChecked() == False
            and self.cconj_checkbox.isChecked() == False and self.det_checkbox.isChecked() == False
            and self.num_checkbox.isChecked() == False and self.part_checkbox.isChecked() == False
            and self.pron_checkbox.isChecked() == False and self.sconj_checkbox.isChecked() == False
            and self.punct_checkbox.isChecked() == False and self.sym_checkbox.isChecked() == False
            and self.x_checkbox.isChecked() == False):
            message_box = QMessageBox()
            message_box.setIcon(QMessageBox.Warning)
            message_box.setWindowTitle("Invalid Parameters")
            message_box.setText("There are currently no parts of speech selected. Please select at least one part of" +
                                " speech to include.")
            message_box.exec_()
            return

        print("Recording parts of speech: " + str(datetime.datetime.now() - start_time))
        self.addPartsOfSpeech()

        print("Checking for stop words: " + str(datetime.datetime.now() - start_time))
        if not self.stop_words_input.text() == "":
            self.addStopWords()

        if not self.stop_words_formatted_correctly:
            message_box = QMessageBox()
            message_box.setIcon(QMessageBox.Warning)
            message_box.setWindowTitle("Stop Words Format Error")
            message_box.setText("The provided stop words file is not formatted correctly. If you choose to" +
                                " continue, there is a chance your stop words will not be properly removed. Are" +
                                " you sure you want to continue?")
            message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            response = message_box.exec_()

            if response == QMessageBox.No:
                return

        print("Saving preference data: " + str(datetime.datetime.now() - start_time))
        self.savePreferenceData()

        if not os.path.exists(self.output_path_input.text() + "/Passages"):
            os.makedirs(self.output_path_input.text() + "/Passages")
            self.passages_directory = self.output_path_input.text() + "/Passages"
        else:
            message_box = QMessageBox()
            message_box.setIcon(QMessageBox.Warning)
            message_box.setWindowTitle("Passages Folder Already Exists")
            message_box.setText("It looks like you already have a folder named \"Passages\" in the specified" +
                                " output directory. If you choose to continue, the contents of this folder will be" +
                                " overwritten. Are you sure you wish to continue?")
            message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            response = message_box.exec_()

            if response == QMessageBox.No:
                self.passages_directory = False
                return
            else:
                self.passages_directory = self.output_path_input.text() + "/Passages"
                for file in os.listdir(self.passages_directory):
                    file_path = os.path.join(self.passages_directory, file)
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path): shutil.rmtree(file_path)
                    except Exception as exception:
                        print(exception)

        print("Formatting corpus:" + str(datetime.datetime.now() - start_time))
        self.formatCorpus()
        if self.temporary_directory_error:
            return

        print("Total preperation time: " + str(datetime.datetime.now() - start_time))
        logging.basicConfig(format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO)
        corpus = corpusObject(self.temporary_directory)

        model = ldamallet.LdaMallet(self.mallet_path_input.text(), corpus, num_topics=int(self.topics_input.text()),
                                    id2word=corpus.dictionary)

        model.print_topics(num_topics=-1, num_words=10)
        shutil.rmtree(self.temporary_directory)

    def savePreferenceData(self):
        preference_data_file = open("files/preference_data.json", "w")
        preference_data = {
            "mallet_path": self.mallet_path_input.text(),
            "input_path": self.input_path_input.text(),
            "output_path": self.output_path_input.text(),
            "stop_words_path": self.stop_words_input.text(),
            "chunk_size": self.chunk_size_input.text(),
            "topics": self.topics_input.text(),
            "parts_of_speech": self.parts_of_speech,
            "language_index": self.language_input.currentIndex()
        }
        json.dump(preference_data, preference_data_file)
        preference_data_file.close()

    def selectMalletPath(self):
        file_dialog = QFileDialog()

        file_dialog.setFileMode(QFileDialog.ExistingFile)
        selected_file = file_dialog.getOpenFileName(caption="Select MALLET Path")
        self.mallet_path_input.setText(selected_file[0])

    def selectInputPath(self):
        file_dialog = QFileDialog()

        file_dialog.setFileMode(QFileDialog.Directory)
        selected_file = file_dialog.getExistingDirectory(caption="Select Input Path")
        self.input_path_input.setText(selected_file)

    def selectOutputPath(self):
        file_dialog = QFileDialog()

        file_dialog.setFileMode(QFileDialog.Directory)
        selected_file = file_dialog.getExistingDirectory(caption="Select Output Path")
        self.output_path_input.setText(selected_file)

    def selectStopWordsPath(self):
        file_dialog = QFileDialog()

        file_dialog.setFileMode(QFileDialog.ExistingFile)
        selected_file = file_dialog.getOpenFileName(caption="Select Stop Words Path")
        self.stop_words_input.setText(selected_file[0])

    def chunkCorpus(self, corpus, number):
        for i in range(0, len(corpus), number):
            yield corpus[i:i + number]

    def formatCorpus(self):
        if not os.path.exists(self.output_path_input.text() + "/Temp"):
            os.makedirs(self.output_path_input.text() + "/Temp")
            self.temporary_directory = self.output_path_input.text() + "/Temp"
            self.temporary_directory_error = False
        else:
            message_box = QMessageBox()
            message_box.setIcon(QMessageBox.Warning)
            message_box.setWindowTitle("Temp Folder Already Exists")
            message_box.setText("It looks like you already have a folder named \"Temp\" in the specified" +
                                " output directory. If you continue, the contents of this folder will be deleted." +
                                " Are you sure you wish to continue?")
            message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            response = message_box.exec_()

            if response == QMessageBox.No:
                self.temporary_directory_error = False
                return
            else:
                self.temporary_directory = self.output_path_input.text() + "/Temp"
                self.temporary_directory = self.output_path_input.text() + "/Temp"
                for file in os.listdir(self.temporary_directory):
                    file_path = os.path.join(self.temporary_directory, file)
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                    except Exception as exception:
                        print(exception)

        for subdirectory, directories, files in os.walk(self.input_path_input.text()):
            for file in files:
                file_name = os.path.splitext(file)[0]
                file_path = os.path.join(subdirectory, file)

                working_file = open(file_path, encoding="utf-8", errors="ignore")
                working_file_text = working_file.read()
                working_file_text = working_file_text.lower().rstrip("/n")
                if not self.punct_checkbox.isChecked():
                    working_file_text = "".join(i for i in working_file_text if i not in string.punctuation)
                working_file.close()

                if self.language_input.currentText() == "Danish":
                    stemmer = SnowballStemmer("danish")
                    tagger = Tagger(language="da")

                elif self.language_input.currentText() == "Norwegian":
                    stemmer = SnowballStemmer("norwegian")
                    tagger = Tagger(language="no")

                elif self.language_input.currentText() == "Swedish":
                    stemmer = SnowballStemmer("swedish")
                    tagger = Tagger(language="sv-2")

                else:
                    stemmer = SnowballStemmer("english")
                    tagger = Tagger(language="en-2")

                tagged_text = tagger.tag(working_file_text)
                chunks = list(self.chunkCorpus(tagged_text, int(self.chunk_size_input.text())))

                chunk_number = 1
                for chunk in chunks:
                    chunked_file = open(self.passages_directory + "/" + file_name + "_" + str(chunk_number) +
                                        ".txt", "w")
                    for tag in chunk:
                        chunked_file.write(tag[0])
                    chunked_file.close()

                    chunked_file = open(self.temporary_directory + "/" + file_name + "_" + str(chunk_number) +
                                        ".txt", "w")
                    for tag in chunk:
                        if tag[1] in self.parts_of_speech:
                            if tag[0] in self.stop_words:
                                pass
                            else:
                                stemmed_tag = stemmer.stem(tag[0])
                                chunked_file.write(stemmed_tag + " ")
                    chunked_file.close()
                    chunk_number += 1

    def addPartsOfSpeech(self):
        if self.adj_checkbox.isChecked():
            self.parts_of_speech.append("ADJ")
        if self.adv_checkbox.isChecked():
            self.parts_of_speech.append("ADV")
        if self.intj_checkbox.isChecked():
            self.parts_of_speech.append("INTJ")
        if self.noun_checkbox.isChecked():
            self.parts_of_speech.append("NOUN")
        if self.propn_checkbox.isChecked():
            self.parts_of_speech.append("PROPN")
        if self.verb_checkbox.isChecked():
            self.parts_of_speech.append("VERB")
        if self.adp_checkbox.isChecked():
            self.parts_of_speech.append("ADP")
        if self.aux_checkbox.isChecked():
            self.parts_of_speech.append("AUX")
        if self.cconj_checkbox.isChecked():
            self.parts_of_speech.append("CCONJ")
        if self.det_checkbox.isChecked():
            self.parts_of_speech.append("DET")
        if self.num_checkbox.isChecked():
            self.parts_of_speech.append("NUM")
        if self.part_checkbox.isChecked():
            self.parts_of_speech.append("PART")
        if self.pron_checkbox.isChecked():
            self.parts_of_speech.append("PRON")
        if self.sconj_checkbox.isChecked():
            self.parts_of_speech.append("SCONJ")
        if self.punct_checkbox.isChecked():
            self.parts_of_speech.append("PUNCT")
        if self.sym_checkbox.isChecked():
            self.parts_of_speech.append("SYM")
        if self.x_checkbox.isChecked():
            self.parts_of_speech.append("X")

    def addStopWords(self):
        with open(self.stop_words_input.text()) as stop_words_file:
            for line in stop_words_file:
                if line.startswith("#"):
                    pass
                elif len(line.split()) > 1:
                    self.stop_words_formatted_correctly = False
                    line = line.replace(",", "")
                    words = line.split(" ")
                    for word in words:
                        self.stop_words.append(word)
                else:
                    self.stop_words_formatted_correctly = True
                    self.stop_words.append(line)
            stop_words_file.close()


"""=================================================="""
"""                       MAIN                       """
"""=================================================="""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QtWidgets.QWidget()
    ui = Ui_main_window()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec_())

"""=================================================="""
"""                       EOF                        """
"""=================================================="""
