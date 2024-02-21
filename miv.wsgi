import sys

# Add your project directory to the sys.path
project_home = '/opt/flask-apps/miv-test'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Import your Dash app instance from the app file
from Market_Inefficiency import app as application
