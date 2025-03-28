""" 
Author : A.I Instaraj
__retro__ : Information Systems
"""

from flask import *

import sys

from werkzeug.security import *

sys.path.insert(0,'../../')

logic_ = Blueprint('logic',
            import_name='__name__',
            static_folder='./src',
            template_folder='./src/templates'
            )
