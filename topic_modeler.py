"""=================================================="""
"""                  TOPIC MODELER                   """
"""=================================================="""
""" AUTHOR: Brady Hammond                            """
""" CREATED: 12/17/16                                """
""" EDITED BY: Brady Hammond                         """
""" EDITED: 06/29/17                                 """
"""=================================================="""
"""                    FILE SETUP                    """
"""=================================================="""

from collections import Counter
from corpus import corpusObject
import csv
import datetime
from gensim.models.wrappers import ldamallet
from gensim.models import ldamodel
import help
import io
import json
import logging
import multiprocessing
from nltk import word_tokenize
import os
from process import fileProcessor
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileDialog
import shutil
from visualization import visualizerObject

"""=================================================="""
"""                CLASS DEFINITIONS                 """
"""=================================================="""

class HelpWindow(QtWidgets.QDialog, help.Ui_help_dialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

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
        self.byu_humanities_logo.setPixmap(QtGui.QPixmap("logo.png"))
        self.byu_humanities_logo.setAlignment(QtCore.Qt.AlignCenter)
        self.byu_humanities_logo.setObjectName("byu_humanities_logo")
        self.grid_layout_main.addWidget(self.byu_humanities_logo, 0, 0, 1, 1)

        self.quit_button = QtWidgets.QPushButton(self.grid_layout_widget_I)
        self.quit_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.quit_button.setObjectName("quit_button")
        self.quit_button.clicked.connect(main_window.close)
        self.grid_layout_main.addWidget(self.quit_button, 1, 3, 1, 1)

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
        icon.addPixmap(QtGui.QPixmap("file.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
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
        self.grid_layout_widget_III.setGeometry(QtCore.QRect(360, 22, 191, 281))
        self.grid_layout_widget_III.setObjectName("gridLayoutWidget_3")
        self.sub_grid_layout_II = QtWidgets.QGridLayout(self.grid_layout_widget_III)
        self.sub_grid_layout_II.setContentsMargins(0, 0, 0, 0)
        self.sub_grid_layout_II.setObjectName("sub_grid_layout_II")

        self.sconj_checkbox = QtWidgets.QCheckBox(self.grid_layout_widget_III)
        self.sconj_checkbox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.sconj_checkbox.setObjectName("sconj_checkbox")
        self.sub_grid_layout_II.addWidget(self.sconj_checkbox, 7, 2, 1, 1)

        self.pron_checkbox = QtWidgets.QCheckBox(self.grid_layout_widget_III)
        self.pron_checkbox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pron_checkbox.setObjectName("pron_checkbox")
        self.sub_grid_layout_II.addWidget(self.pron_checkbox, 6, 2, 1, 1)

        self.num_checkbox = QtWidgets.QCheckBox(self.grid_layout_widget_III)
        self.num_checkbox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.num_checkbox.setObjectName("num_checkbox")
        self.sub_grid_layout_II.addWidget(self.num_checkbox, 4, 2, 1, 1)

        self.cconj_checkbox = QtWidgets.QCheckBox(self.grid_layout_widget_III)
        self.cconj_checkbox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.cconj_checkbox.setObjectName("cconj_checkbox")
        self.sub_grid_layout_II.addWidget(self.cconj_checkbox, 2, 2, 1, 1)

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
        self.sub_grid_layout_II.addWidget(self.det_checkbox, 3, 2, 1, 1)

        self.aux_checkbox = QtWidgets.QCheckBox(self.grid_layout_widget_III)
        self.aux_checkbox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.aux_checkbox.setObjectName("aux_checkbox")
        self.sub_grid_layout_II.addWidget(self.aux_checkbox, 1, 2, 1, 1)

        self.propn_checkbox = QtWidgets.QCheckBox(self.grid_layout_widget_III)
        self.propn_checkbox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.propn_checkbox.setObjectName("propn_checkbox")
        self.sub_grid_layout_II.addWidget(self.propn_checkbox, 5, 1, 1, 1)

        self.part_checkbox = QtWidgets.QCheckBox(self.grid_layout_widget_III)
        self.part_checkbox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.part_checkbox.setObjectName("part_checkbox")
        self.sub_grid_layout_II.addWidget(self.part_checkbox, 5, 2, 1, 1)

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
        self.help_button.clicked.connect(self.openHelpDialog)
        self.sub_grid_layout_II.addWidget(self.help_button, 10, 1, 1, 2)
        self.grid_layout_main.addWidget(self.parameters_box, 0, 1, 1, 5)

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
        self.version_label.setObjectName("version_label")
        self.grid_layout_main.addWidget(self.version_label, 1, 5, 1, 1)

        self.progress = 0
        self.word_frequencies = Counter()
        self.top_point_one_percent = []
        self.top_point_two_five_percent = []
        self.top_point_five_percent = []
        self.documents = []
        self.distributions = []
        self.parts_of_speech = []
        self.stop_words = []
        self.temporary_directory = ""
        self.passages_directory = ""
        self.word_clouds_directory = ""
        self.scatter_plot_directory = ""
        self.temporary_directory_error = False
        self.stop_words_formatted_correctly = True
        self.mallet = True

        self.retranslateUi(main_window)
        self.setCheckboxes()
        self.setLanguage()
        QtCore.QMetaObject.connectSlotsByName(main_window)

    # ==================================================

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
        self.sconj_checkbox.setText(_translate("main_window", "SCONJ"))
        self.pron_checkbox.setText(_translate("main_window", "PRON"))
        self.num_checkbox.setText(_translate("main_window", "NUM"))
        self.cconj_checkbox.setText(_translate("main_window", "CCONJ"))
        self.adj_checkbox.setText(_translate("main_window", "ADJ"))
        self.adv_checkbox.setText(_translate("main_window", "ADV"))
        self.det_checkbox.setText(_translate("main_window", "DET"))
        self.aux_checkbox.setText(_translate("main_window", "AUX"))
        self.propn_checkbox.setText(_translate("main_window", "PROPN"))
        self.part_checkbox.setText(_translate("main_window", "PART"))
        self.intj_checkbox.setText(_translate("main_window", "INTJ"))
        self.verb_checkbox.setText(_translate("main_window", "VERB"))
        self.part_of_speech_label.setText(_translate("main_window", "Parts of Speech:"))
        self.noun_checkbox.setText(_translate("main_window", "NOUN"))
        self.adp_checkbox.setText(_translate("main_window", "ADP"))
        self.help_button.setText(_translate("main_window", "Help"))
        self.version_label.setText(_translate("main_window", "Version 1.1.1"))

        preference_data_file = io.open("preference_data.json", "r")
        preference_data = json.load(preference_data_file)
        self.mallet_path_input.setText(_translate("main_window", preference_data["mallet_path"]))
        self.input_path_input.setText(_translate("main_window", preference_data["input_path"]))
        self.output_path_input.setText(_translate("main_window", preference_data["output_path"]))
        self.stop_words_input.setText(_translate("main_window", preference_data["stop_words_path"]))
        self.chunk_size_input.setText(_translate("main_window", preference_data["chunk_size"]))
        self.topics_input.setText(_translate("main_window", preference_data["topics"]))
        preference_data_file.close()

    # ==================================================

    def openHelpDialog(self):
        dialog = HelpWindow(self)
        dialog.exec_()

    # ==================================================

    def setCheckboxes(self):
        preference_data_file = io.open("preference_data.json", "r")
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

        preference_data_file.close()

    # ==================================================

    def setLanguage(self):
        preference_data_file = io.open("preference_data.json", "r")
        preference_data = json.load(preference_data_file)
        self.language_input.setCurrentIndex(int(preference_data["language_index"]))
        preference_data_file.close()

    # ==================================================

    def runModel(self):
        start_time = datetime.datetime.now()

        print(str(datetime.datetime.now())[:-3] + " : INFO : reseting GUI object variables")
        logging.info("reseting GUI object variables")
        self.progress = 0
        self.word_frequencies = Counter()
        self.top_point_one_percent = []
        self.top_point_two_five_percent = []
        self.top_point_five_percent = []
        self.documents = []
        self.distributions = []
        self.parts_of_speech = []
        self.stop_words = []
        self.temporary_directory = ""
        self.passages_directory = ""
        self.word_clouds_directory = ""
        self.scatter_plot_directory = ""
        self.temporary_directory_error = False
        self.stop_words_formatted_correctly = True
        self.mallet = True

        print(str(datetime.datetime.now())[:-3] + " : INFO : starting progress bar")
        logging.info("starting progress bar")
        progress_bar = QtWidgets.QProgressDialog("Running Topic Model...", "Cancel", 0, 100, self)
        progress_bar.setValue(self.progress)
        progress_bar.setCancelButton(None)
        progress_bar.setWindowModality(QtCore.Qt.WindowModal)
        progress_bar.resize(400, 50)
        progress_bar.show()

        print(str(datetime.datetime.now())[:-3] + " : INFO : checking input fields")
        logging.info("checking input fields")
        if self.mallet_path_input.text() == "":
            message_box = QMessageBox()
            message_box.setIcon(QMessageBox.Warning)
            message_box.setWindowTitle("Missing MALLET Path")
            message_box.setText("You have not added a path to MALLET. If you choose to continue, gensim's LDA Model" +
                                " will be used instead. Scatter plots are unavailable when using gensim's LDA Model" +
                                ", and document distributions only show the most relevant topics. Are you sure you" +
                                " wish to continue?")
            message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            response = message_box.exec_()

            if response == QMessageBox.No:
                progress_bar.close()
                return
            self.mallet = False

        elif not (os.path.isfile(self.mallet_path_input.text()) and os.access(self.mallet_path_input.text(), os.X_OK)):
            message_box = QMessageBox()
            message_box.setIcon(QMessageBox.Warning)
            message_box.setWindowTitle("Invalid Parameters")
            message_box.setText("The MALLET path doesn't seem quite right. Please enter a valid path to MALLET.")
            message_box.exec_()

            self.mallet_path_input.setFocus()
            progress_bar.close()
            return

        if self.input_path_input.text() == "":
            message_box = QMessageBox()
            message_box.setIcon(QMessageBox.Warning)
            message_box.setWindowTitle("Invalid Parameters")
            message_box.setText("The input path field is currently empty. Please enter a valid input folder.")
            message_box.exec_()

            self.input_path_input.setFocus()
            progress_bar.close()
            return

        elif not os.path.isdir(self.input_path_input.text()):
            message_box = QMessageBox()
            message_box.setIcon(QMessageBox.Warning)
            message_box.setWindowTitle("Invalid Parameters")
            message_box.setText("The input path doesn't seem quite right. Please enter a valid input folder.")
            message_box.exec_()

            self.input_path_input.setFocus()
            progress_bar.close()
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
            progress_bar.close()
            return

        if self.output_path_input.text() == "":
            message_box = QMessageBox()
            message_box.setIcon(QMessageBox.Warning)
            message_box.setWindowTitle("Invalid Parameters")
            message_box.setText("The output path field is currently empty. Please enter a valid path output folder.")
            message_box.exec_()

            self.output_path_input.setFocus()
            progress_bar.close()
            return

        elif not os.path.isdir(self.output_path_input.text()):
            message_box = QMessageBox()
            message_box.setIcon(QMessageBox.Warning)
            message_box.setWindowTitle("Invalid Parameters")
            message_box.setText("The output path doesn't seem quite right. Please enter a valid output folder.")
            message_box.exec_()

            self.output_path_input.setFocus()
            progress_bar.close()
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
            progress_bar.close()
            return

        elif not self.stop_words_input.text().endswith(".txt") and self.stop_words_input.text() != "":
            message_box = QMessageBox()
            message_box.setIcon(QMessageBox.Warning)
            message_box.setWindowTitle("Invalid Parameters")
            message_box.setText("The stop words file doesn't seem quite right. Please enter a valid stop words file.")
            message_box.exec_()

            self.stop_words_input.setFocus()
            progress_bar.close()
            return

        if self.chunk_size_input.text() == "":
            message_box = QMessageBox()
            message_box.setIcon(QMessageBox.Warning)
            message_box.setWindowTitle("Invalid Parameters")
            message_box.setText("The chunk size field is currently empty. Please enter a valid chunk size.")
            message_box.exec_()

            self.chunk_size_input.setFocus()
            progress_bar.close()
            return

        elif not self.chunk_size_input.text().isdigit():
            if self.chunk_size_input.text().lower() == "document":
                pass
            else:
                message_box = QMessageBox()
                message_box.setIcon(QMessageBox.Warning)
                message_box.setWindowTitle("Invalid Parameters")
                message_box.setText("The chunk size field doesn't seem quite right. Please remember that chunk size" +
                                    " should be a number or \"Document\".")
                message_box.exec_()

                self.chunk_size_input.setFocus()
                progress_bar.close()
                return

        if self.topics_input.text() == "":
            message_box = QMessageBox()
            message_box.setIcon(QMessageBox.Warning)
            message_box.setWindowTitle("Invalid Parameters")
            message_box.setText("The topics field is currently empty. Please enter a valid number of topics.")
            message_box.exec_()

            self.topics_input.setFocus()
            progress_bar.close()
            return

        elif not self.topics_input.text().isdigit():
            message_box = QMessageBox()
            message_box.setIcon(QMessageBox.Warning)
            message_box.setWindowTitle("Invalid Parameters")
            message_box.setText("The topics field doesn't seem quite right. Please remember that topics should be" +
                                " a number.")
            message_box.exec_()

            self.topics_input.setFocus()
            progress_bar.close()
            return

        if (self.adj_checkbox.isChecked() == False and self.adv_checkbox.isChecked() == False
            and self.intj_checkbox.isChecked() == False and self.noun_checkbox.isChecked() == False
            and self.propn_checkbox.isChecked() == False and self.verb_checkbox.isChecked() == False
            and self.adp_checkbox.isChecked() == False and self.aux_checkbox.isChecked() == False
            and self.cconj_checkbox.isChecked() == False and self.det_checkbox.isChecked() == False
            and self.num_checkbox.isChecked() == False and self.part_checkbox.isChecked() == False
            and self.pron_checkbox.isChecked() == False and self.sconj_checkbox.isChecked() == False):
            message_box = QMessageBox()
            message_box.setIcon(QMessageBox.Warning)
            message_box.setWindowTitle("Invalid Parameters")
            message_box.setText("There are currently no parts of speech selected. Please select at least one part of" +
                                " speech to include.")
            message_box.exec_()
            progress_bar.close()
            return

        self.progress += 1
        progress_bar.setValue(self.progress)
        print(str(datetime.datetime.now())[:-3] + " : INFO : recording parts of speech")
        logging.info("recording parts of speech")
        self.addPartsOfSpeech()

        self.progress += 1
        progress_bar.setValue(self.progress)
        print(str(datetime.datetime.now())[:-3] + " : INFO : checking for stop words")
        logging.info("checking for stop words")
        if not self.stop_words_input.text() == "":
            print(str(datetime.datetime.now())[:-3] + " : INFO : analyzing stop words")
            self.addStopWords()

        if not self.stop_words_formatted_correctly:
            message_box = QMessageBox()
            message_box.setIcon(QMessageBox.Warning)
            message_box.setWindowTitle("Stop Words Format Error")
            message_box.setText("The provided stop words file is not formatted correctly. If you choose to" +
                                " continue, there is a chance your stop words will not be properly removed. Are" +
                                " you sure you wish to continue?")
            message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            response = message_box.exec_()

            if response == QMessageBox.No:
                progress_bar.close()
                return

        self.progress += 1
        progress_bar.setValue(self.progress)
        print(str(datetime.datetime.now())[:-3] + " : INFO : saving preference data")
        logging.info("saving preference data")
        self.savePreferenceData()

        if not self.chunk_size_input.text().isalpha():
            if not os.path.exists(self.output_path_input.text() + "/Passages"):
                os.makedirs(self.output_path_input.text() + "/Passages")
                self.passages_directory = self.output_path_input.text() + "/Passages"

            else:
                message_box = QMessageBox()
                message_box.setIcon(QMessageBox.Warning)
                message_box.setWindowTitle("Passages Folder Already Exists")
                message_box.setText("It looks like you already have a folder named \"Passages\" in the specified" +
                                    " output directory. If you choose to continue, the contents of this folder will" +
                                    " be overwritten. Are you sure you wish to continue?")
                message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                response = message_box.exec_()

                if response == QMessageBox.No:
                    progress_bar.close()
                    return
                else:
                    self.passages_directory = self.output_path_input.text() + "/Passages"
                    for file in os.listdir(self.passages_directory):
                        file_path = os.path.join(self.passages_directory, file)
                        try:
                            if os.path.isfile(file_path):
                                os.unlink(file_path)
                            elif os.path.isdir(file_path): shutil.rmtree(file_path, ignore_errors=True)
                        except Exception as exception:
                            #print(exception)
                            logging.log(exception)

        self.progress += 1
        progress_bar.setValue(self.progress)
        print(str(datetime.datetime.now())[:-3] + " : INFO : formatting corpus")
        logging.info("formatting corpus")

        self.formatCorpus(progress_bar)
        if self.temporary_directory_error:
            progress_bar.close()
            return

        self.progress += 24
        progress_bar.setValue(self.progress)
        print(str(datetime.datetime.now())[:-3] + " : INFO : starting topic model")
        logging.info("starting topic model")

        logging.basicConfig(format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO)
        corpus = corpusObject(self.temporary_directory)

        if self.mallet == True:
            model = ldamallet.LdaMallet(self.mallet_path_input.text(), corpus, num_topics=int(self.topics_input.text()),
                                    id2word=corpus.dictionary)
        else:
            model = ldamodel.LdaModel(corpus=corpus, num_topics=int(self.topics_input.text()),
                                      id2word=corpus.dictionary, passes=10)

        self.progress += 16
        progress_bar.setValue(self.progress)
        print(str(datetime.datetime.now())[:-3] + " : INFO : saving topics")
        logging.info("saving topics")

        if os.path.isfile(self.output_path_input.text() + "/topics.csv"):
            message_box = QMessageBox()
            message_box.setIcon(QMessageBox.Warning)
            message_box.setWindowTitle("Topics Spreadsheet Already Exists")
            message_box.setText("It looks like you already have a file named \"topics.csv\" in the specified" +
                                " output directory. If you choose to continue, the contents of this folder will be" +
                                " overwritten. Are you sure you wish to continue?")
            message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            response = message_box.exec_()

            if response == QMessageBox.No:
                shutil.rmtree(self.temporary_directory, ignore_errors=True)
                progress_bar.close()
                return
        output_file = io.open(self.output_path_input.text() + "/topics.csv", "w", encoding="utf-8")
        csv_writer = csv.writer(output_file)

        for i in range(0, int(self.topics_input.text())):
            if self.mallet == True:
                row_body = model.show_topic(i, num_words=20)
            else:
                row_body = model.show_topic(i, topn=20)
            row_body.insert(0, "Topic " + str(i + 1))
            csv_writer.writerow(row_body)

        output_file.close()

        self.progress += 4
        progress_bar.setValue(self.progress)
        print(str(datetime.datetime.now())[:-3] + " : INFO : saving distributions")
        logging.info("saving distributions")

        if os.path.isfile(self.output_path_input.text() + "/distributions.csv"):
            message_box = QMessageBox()
            message_box.setIcon(QMessageBox.Warning)
            message_box.setWindowTitle("Distributions Spreadsheet Already Exists")
            message_box.setText("It looks like you already have a file named \"distributions.csv\" in the specified" +
                                " output directory. If you choose to continue, the contents of this folder will be" +
                                " overwritten. Are you sure you wish to continue?")
            message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            response = message_box.exec_()

            if response == QMessageBox.No:
                shutil.rmtree(self.temporary_directory, ignore_errors=True)
                progress_bar.close()
                return

        output_file = io.open(self.output_path_input.text() + "/distributions.csv", "w", encoding="utf-8")
        csv_writer = csv.writer(output_file)

        if self.mallet == True:
            self.distributions = [distribution for distribution in model.load_document_topics()]

        else:
            for subdirectory, directories, files in os.walk(self.temporary_directory):
                for file in files:
                    if not file.startswith('.'):
                        file_path = os.path.join(self.temporary_directory, file)
                        try:
                            if os.path.isfile(file_path):
                                working_file = io.open(file_path, "r", encoding="utf-8", errors="ignore")
                                self.distributions.append(model.get_document_topics(corpus.dictionary.doc2bow(
                                    word_tokenize(working_file.read()))))

                        except Exception as exception:
                            print(exception)
                            logging.info(exception)

        if self.chunk_size_input.text().isalpha():
            for subdirectory, directories, files in os.walk(self.input_path_input.text()):
                for file in files:
                    if not file.startswith('.'):
                        self.documents.append(os.path.splitext(file)[0])

        else:
            for subdirectory, directories, files in os.walk(self.temporary_directory):
                for file in files:
                    if not file.startswith('.'):
                        self.documents.append(os.path.splitext(file)[0])

        for i in range(0, (len(self.distributions) - 1)):
            row_body = list(self.distributions[i])
            row_body.insert(0, self.documents[i])
            csv_writer.writerow(row_body)

        output_file.close()

        self.progress += 4
        progress_bar.setValue(self.progress)

        visualizer = visualizerObject(self.top_point_one_percent, self.top_point_two_five_percent,
                                self.top_point_five_percent, self.mallet,
                                self.word_clouds_directory, self.distributions, self.documents,
                                self.scatter_plot_directory)
        if self.mallet == True:
            print(str(datetime.datetime.now())[:-3] + " : INFO : starting scatter plot generation")
            logging.info("starting scatter plot generation")
            if not os.path.exists(self.output_path_input.text() + "/Scatter_Plots"):
                os.makedirs(self.output_path_input.text() + "/Scatter_Plots")
                self.scatter_plot_directory = self.output_path_input.text() + "/Scatter_Plots"
                visualizer.setScatterPlotDirectory(self.scatter_plot_directory)
            else:
                message_box = QMessageBox()
                message_box.setIcon(QMessageBox.Warning)
                message_box.setWindowTitle("Scatter Plot Folder Already Exists")
                message_box.setText("It looks like you already have a folder named \"Scatter_Plots\" in the specified" +
                                    " output directory. If you choose to continue, the contents of this folder will" +
                                    " be overwritten. Are you sure you wish to continue?")
                message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                response = message_box.exec_()

                if response == QMessageBox.No:
                    shutil.rmtree(self.temporary_directory, ignore_errors=True)
                    progress_bar.close()
                    return
                else:
                    self.scatter_plot_directory = self.output_path_input.text() + "/Scatter_Plots"
                    visualizer.setScatterPlotDirectory(self.scatter_plot_directory)
                    for file in os.listdir(self.scatter_plot_directory):
                        file_path = os.path.join(self.scatter_plot_directory, file)
                        try:
                            if os.path.isfile(file_path):
                                os.unlink(file_path)
                            elif os.path.isdir(file_path):
                                shutil.rmtree(file_path, ignore_errors=True)
                        except Exception as exception:
                            print(exception)
                            logging.info(exception)

            increment = 24/(int(self.topics_input.text()))
            for i in range(int(self.topics_input.text())):
                visualizer.generateScatterPlots(i)
                self.progress += increment
                progress_bar.setValue(self.progress)

        else:
            self.progress += 24
            progress_bar.setValue(self.progress)

        print(str(datetime.datetime.now())[:-3] + " : INFO : starting word cloud generation")
        logging.info("starting word cloud generation")

        if not os.path.exists(self.output_path_input.text() + "/Word_Clouds"):
            os.makedirs(self.output_path_input.text() + "/Word_Clouds")
            self.word_clouds_directory = self.output_path_input.text() + "/Word_Clouds"
            visualizer.setWordCloudDirectory(self.word_clouds_directory)
        else:
            message_box = QMessageBox()
            message_box.setIcon(QMessageBox.Warning)
            message_box.setWindowTitle("Word Cloud Folder Already Exists")
            message_box.setText("It looks like you already have a folder named \"Word_Clouds\" in the specified" +
                                " output directory. If you choose to continue, the contents of this folder will be" +
                                " overwritten. Are you sure you wish to continue?")
            message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            response = message_box.exec_()

            if response == QMessageBox.No:
                shutil.rmtree(self.temporary_directory, ignore_errors=True)
                progress_bar.close()
                return
            else:
                self.word_clouds_directory = self.output_path_input.text() + "/Word_Clouds"
                visualizer.setWordCloudDirectory(self.word_clouds_directory)
                for file in os.listdir(self.word_clouds_directory):
                    file_path = os.path.join(self.word_clouds_directory, file)
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path): shutil.rmtree(file_path, ignore_errors=True)
                    except Exception as exception:
                        print(exception)
                        logging.info(exception)

        # Replaced with Pool
        '''jobs = []
        for i in range(int(self.topics_input.text())):
            process = multiprocessing.Process(target=self.generateWordClouds, args=(i, model))
            jobs.append(process)
            process.start()

        for job in jobs:
            job.join()'''

        pool = multiprocessing.Pool(processes=multiprocessing.cpu_count() - 2 or 1)
        for i in range(int(self.topics_input.text())):
            pool.apply_async(visualizer.generateWordClouds, args=(i, model))
        pool.close()
        pool.join()


        self.progress += 25
        progress_bar.setValue(self.progress)
        shutil.rmtree(self.temporary_directory, ignore_errors=True)
        progress_bar.close()
        print(str(datetime.datetime.now())[:-3] + " : INFO : final runtime: " +
              str(datetime.datetime.now() - start_time))
        logging.info("final runtime: " + str(datetime.datetime.now() - start_time))

    # ==================================================

    # Moved to visualiztion.py
    '''def generateWordClouds(self, number, model):
        word_cloud = WordCloud(
            background_color="white",
            max_words=100,
            width=1024,
            height=1024,
        )

        color_to_words = {
            "#2bf72d": self.top_point_one_percent,
            "#9e40ed": self.top_point_two_five_percent,
            "#103ffb": self.top_point_five_percent
        }

        default_color = "black"
        grouped_color_function = word_cloud_color.GroupedColorFunc(color_to_words, default_color)

        if self.mallet == True:
            tuples = model.show_topic(number, num_words=100)
            frequency_dictionary = dict([(entry[1], entry[0]) for entry in tuples])
            for key in frequency_dictionary.keys():
                if frequency_dictionary[key] == 0.0:
                    frequency_dictionary[key] = 0.00001

        else:
            tuples = model.show_topic(number, topn=100)
            frequency_dictionary = dict(tuples)
            for key in frequency_dictionary.keys():
                if frequency_dictionary[key] == 0.0:
                    frequency_dictionary[key] = 0.00001
        try:
            word_cloud.generate_from_frequencies(frequency_dictionary)
            word_cloud.recolor(color_func=grouped_color_function)
            word_cloud.to_file(self.word_clouds_directory + "/word_cloud_" + str(number + 1) + ".png")
        except Exception as exception:
            logging.info(exception)'''

    # ==================================================

    # Moved to visualiztion.py
    '''def generateScatterPlots(self, number):
        document_saturations = []

        for distribution in self.distributions:
            document_saturations.append(distribution[number][1])

        x = range(0, len(self.documents))

        figure = pyplot.figure(figsize=(10,5), dpi=100)
        figure.suptitle("Topic " + str(number + 1) + " Distribution", fontsize=14)
        figure.add_subplot(1, 1, 1)

        ---> *** Add Document Titles to Scatter Plots ***
        if self.chunk_size_input.text().lower() == "document":
            pyplot.xticks(x, self.documents, rotation="vertical")
        else:
            ticks = []
            for i in range(len(self.documents) - 1):
                if i == (len(self.documents) - 1):
                    ticks.append(re.sub("_\d*$", "", self.documents[i]))
                elif re.sub("_\d*$", "", self.documents[i]) == re.sub("_\d*$", "", self.documents[i+1]):
                    ticks.append(self.documents[i])
                else:
                    ticks.append(re.sub("_\d*$", "", self.documents[i]))

            pyplot.xticks(x, ticks, rotation="vertical")

            axes = pyplot.axes()
            for label in axes.xaxis.get_ticklabels():
                if re.search("_\d*$", label.get_text()):
                    label.set_visible(False)
        
            axes.xaxis.set_ticks_position("none")
        <---
        for label in pyplot.axes().xaxis.get_ticklabels():
            label.set_visible(False)

        pyplot.axes().xaxis.set_ticks_position("none")

        pyplot.scatter(x, document_saturations, alpha=0.8, color="#3097d1")
        pyplot.savefig(self.scatter_plot_directory + "/scatter_plot_" + str(number + 1) + ".png")
        pyplot.clf()
        pyplot.close()'''

    # ==================================================

    def savePreferenceData(self):
        preference_data_file = io.open("preference_data.json", "w")
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

    # ==================================================

    def selectMalletPath(self):
        file_dialog = QFileDialog()

        file_dialog.setFileMode(QFileDialog.ExistingFile)
        selected_file = file_dialog.getOpenFileName(caption="Select MALLET Path")
        self.mallet_path_input.setText(selected_file[0])

    # ==================================================

    def selectInputPath(self):
        file_dialog = QFileDialog()

        file_dialog.setFileMode(QFileDialog.Directory)
        selected_file = file_dialog.getExistingDirectory(caption="Select Input Path")
        self.input_path_input.setText(selected_file)

    # ==================================================

    def selectOutputPath(self):
        file_dialog = QFileDialog()

        file_dialog.setFileMode(QFileDialog.Directory)
        selected_file = file_dialog.getExistingDirectory(caption="Select Output Path")
        self.output_path_input.setText(selected_file)

    # ==================================================

    def selectStopWordsPath(self):
        file_dialog = QFileDialog()

        file_dialog.setFileMode(QFileDialog.ExistingFile)
        selected_file = file_dialog.getOpenFileName(caption="Select Stop Words Path")
        self.stop_words_input.setText(selected_file[0])

    # ==================================================

    # Moved to process.py
    '''def chunkCorpus(self, corpus, number):
        for i in range(0, len(corpus), number):
                yield corpus[i:i + number]'''

    # ==================================================

    def formatCorpus(self, progress_bar):
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
                progress_bar.close()
                return
            else:
                self.temporary_directory = self.output_path_input.text() + "/Temp"
                self.temporary_directory = self.output_path_input.text() + "/Temp"
                for file in os.listdir(self.temporary_directory):
                    if not file.startswith('.'):
                        file_path = os.path.join(self.temporary_directory, file)
                        try:
                            if os.path.isfile(file_path):
                                os.unlink(file_path)
                            elif os.path.isdir(file_path):
                                shutil.rmtree(file_path, ignore_errors=True)
                        except Exception as exception:
                            print(exception)

        # Replaced with Pool
        '''
        increment = 24/len([file for file in os.listdir(self.input_path_input.text()) if not file.startswith('.')])
        '''
        '''for subdirectory, directories, files in os.walk(self.input_path_input.text()):
            jobs = []
            for file in files:
                if not file.startswith('.'):
                    process = multiprocessing.Process(target=self.processFile, args=(subdirectory, file))
                    jobs.append(process)
                    process.start()
            for job in jobs:
                job.join()'''

        print(str(datetime.datetime.now())[:-3] + " : INFO : starting file processor")
        logging.info("starting file processor")

        if self.chunk_size_input.text().isalpha():
            file_processor = fileProcessor(self.language_input.currentText(), self.chunk_size_input.text().lower(),
                                self.passages_directory, self.temporary_directory, self.parts_of_speech,
                                self.stop_words)
        else:
            file_processor = fileProcessor(self.language_input.currentText(), self.chunk_size_input.text(),
                                           self.passages_directory, self.temporary_directory, self.parts_of_speech,
                                           self.stop_words)
        for subdirectory, directories, files in os.walk(self.input_path_input.text()):
            pool = multiprocessing.Pool(processes=multiprocessing.cpu_count()-2 or 1)
            for file in files:
                pool.apply_async(file_processor.processFile, args=(subdirectory, file))
            pool.close()
            pool.join()

        for file in os.listdir(self.temporary_directory):
            if not file.startswith('.'):
                file_path = os.path.join(self.temporary_directory, file)
                try:
                    if os.path.isfile(file_path):
                        working_file = io.open(file_path, "r", encoding="utf-8", errors="ignore")
                        for line in working_file:
                            self.word_frequencies.update(line.split())

                except Exception as exception:
                    print(exception)

        words_total = len(self.word_frequencies)
        point_one_percent = int(float(words_total) * 0.001)
        point_two_five_percent = int(float(words_total) * 0.0025)
        point_five_percent = int(float(words_total) * 0.005)

        for word, frequency in self.word_frequencies.most_common(point_one_percent):
            self.top_point_one_percent.append(word)

        for word, frequency in self.word_frequencies.most_common(point_two_five_percent):
            if not word in self.top_point_one_percent:
                self.top_point_two_five_percent.append(word)

        for word, frequency in self.word_frequencies.most_common(point_five_percent):
            if not word in self.top_point_one_percent:
                if not word in self.top_point_two_five_percent:
                    self.top_point_five_percent.append(word)

    # ==================================================

    # Moved to process.py
    '''def processFile(self, subdirectory, file):
        file_name = os.path.splitext(file)[0]
        file_path = os.path.join(subdirectory, file)

        working_file = io.open(file_path, encoding="utf-8", errors="ignore")
        working_file_text = working_file.read()
        working_file_text = working_file_text.lower().rstrip("/n")

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
            tagger = Tagger(language="en-1")

        tagged_text = tagger.tag(working_file_text)
        if self.chunk_size_input.text().lower() == "document":

            chunked_file = io.open(self.temporary_directory + "/" + file_name + ".txt", "w", encoding="utf-8")
            for tag in tagged_text:
                if tag[1] in self.parts_of_speech:
                    word = re.sub("»|«","", tag[0])
                    word = word.strip(string.punctuation)
                    stemmed_tag = stemmer.stem(word)
                    if stemmed_tag in self.stop_words:
                        pass
                    else:
                        chunked_file.write(stemmed_tag + " ")
            chunked_file.close()

        else:
            chunks = list(self.chunkCorpus(tagged_text, int(self.chunk_size_input.text())))

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
                chunk_number += 1'''

    # ==================================================

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

    # ==================================================

    def addStopWords(self):
        with io.open(self.stop_words_input.text(), encoding="utf-8") as stop_words_file:
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
                    self.stop_words.append(line.strip())
        stop_words_file.close()


"""=================================================="""
"""                       EOF                        """
"""=================================================="""
