"""=================================================="""
"""                  VISUALIZATION                   """
"""=================================================="""
""" AUTHOR: Brady Hammond                            """
""" CREATED: 09/26/17                                """
""" EDITED BY: -----                                 """
""" EDITED: --/--/--                                 """
"""=================================================="""
"""                    FILE SETUP                    """
"""=================================================="""
import logging
import matplotlib.pyplot as pyplot
from wordcloud import WordCloud
import word_cloud_color

"""=================================================="""
"""                CLASS DEFINITIONS                 """
"""=================================================="""

class visualizerObject(object):
    def __init__(self, top_point_one_percent, top_point_two_five_percent, top_point_five_percent, mallet,
                 word_clouds_directory, distributions, documents, scatter_plot_directory):
        self.top_point_one_percent = top_point_one_percent
        self.top_point_two_five_percent = top_point_two_five_percent
        self.top_point_five_percent = top_point_five_percent
        self.mallet = mallet
        self.word_clouds_directory = word_clouds_directory
        self.distributions = distributions
        self.documents = documents
        self.scatter_plot_directory = scatter_plot_directory

    # ==================================================

    def setScatterPlotDirectory(self, scatter_plot_directory):
        self.scatter_plot_directory = scatter_plot_directory

    # ==================================================

    def setWordCloudDirectory(self, word_clouds_directory):
        self.word_clouds_directory = word_clouds_directory

    # ==================================================

    def generateWordClouds(self, number, model):
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
            logging.info(exception)


    # ==================================================

    def generateScatterPlots(self, number):
        document_saturations = []

        for distribution in self.distributions:
            document_saturations.append(distribution[number][1])

        x = range(0, len(self.documents))

        figure = pyplot.figure(figsize=(10, 5), dpi=100)
        figure.suptitle("Topic " + str(number + 1) + " Distribution", fontsize=14)
        figure.add_subplot(1, 1, 1)

        ''' *** Add Document Titles to Scatter Plots ***
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
        '''
        for label in pyplot.axes().xaxis.get_ticklabels():
            label.set_visible(False)

        pyplot.axes().xaxis.set_ticks_position("none")

        pyplot.scatter(x, document_saturations, alpha=0.8, color="#3097d1")
        pyplot.savefig(self.scatter_plot_directory + "/scatter_plot_" + str(number + 1) + ".png")
        pyplot.clf()
        pyplot.close()

"""=================================================="""
"""                       EOF                        """
"""=================================================="""
