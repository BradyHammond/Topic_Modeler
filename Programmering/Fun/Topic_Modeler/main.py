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

import logging
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
import sys
import topic_modeler

"""=================================================="""
"""                CLASS DEFINITIONS                 """
"""=================================================="""

class MainWindow(QtWidgets.QDialog, topic_modeler.Ui_main_window):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

"""=================================================="""
"""                       MAIN                       """
"""=================================================="""

if __name__ == "__main__":
    #logging.basicConfig(format="%(asctime)s : %(levelname)s : %(message)s", filename="/topic_modeler.log", level=logging.INFO)
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

"""=================================================="""
"""                       EOF                        """
"""=================================================="""