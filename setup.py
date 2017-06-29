"""=================================================="""
"""                       SETUP                      """
"""=================================================="""
""" AUTHOR: Brady Hammond                            """
""" CREATED: 12/17/16                                """
""" EDITED BY: Brady Hammond                         """
""" EDITED: 06/29/17                                 """
"""=================================================="""
"""                    FILE SETUP                    """
"""=================================================="""

import macholib
from setuptools import setup

"""=================================================="""
"""                  MACHOLIB PATCH                  """
"""=================================================="""

if macholib.__version__ <= "1.7":
    import macholib.dyld
    import macholib.MachOGraph

    dyld_find_1_7 = macholib.dyld.dyld_find

    def dyld_find(name, loader=None, **kwargs):
        if loader is not None:
            kwargs['loader_path'] = loader
        return dyld_find_1_7(name, **kwargs)
    macholib.MachOGraph.dyld_find = dyld_find

"""=================================================="""
"""                       MAIN                       """
"""=================================================="""

APP = ['main.py']
DATA_FILES = ['resources/images/file.png', 'resources/images/logo.png', 'resources/images/x_icon.png',
              'resources/files/preference_data.json']
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'resources/images/logo.icns',
    'packages': ['PIL', 'PyQt5', 'rippletagger', 'wordcloud'],
    'plist': {
        'CFBundleName': 'Scandinavian Topic Modeler',
        'CFBundleShortVersionString': '1.0.3',
        'CFBundleVersion': '1.0.3',
        'CFBundleIdentifier': 'org.nordicdh.topic.modeler',
        'NSHumanReadableCopyright': '©Brigham Young University 2017',
        'CFBundleDevelopmentRegion': 'English'
    }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)

"""=================================================="""
"""                       EOF                        """
"""=================================================="""