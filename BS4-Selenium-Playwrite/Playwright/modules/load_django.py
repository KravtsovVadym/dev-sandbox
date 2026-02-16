"""
Add the directory of the current file to the path system
for use Django functions and models in the current script
"""

import os
import sys
import django


sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "braincomua_project"))
)

os.environ["DJANGO_SETTINGS_MODULE"] = "braincomua_project.settings"

django.setup()
