"""=================================================="""
"""                       MAIN                       """
"""=================================================="""
""" AUTHOR: Brady Hammond                            """
""" CREATED: 12/17/16                                """
""" EDITED BY: Brady Hammond                         """
""" EDITED: 06/29/17                                 """
"""=================================================="""
"""                    FILE SETUP                    """
"""=================================================="""

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
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

"""=================================================="""
"""                       EOF                        """
"""=================================================="""