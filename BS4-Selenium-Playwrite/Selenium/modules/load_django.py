"""
The script adds the path to the django project,
specifies which settings to use and starts django?
This allows you to run django from a regular Python script
and work with models.

"""

import os
import sys
import django


sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "braincomua_project"))
)

os.environ["DJANGO_SETTINGS_MODULE"] = "braincomua_project.settings"

django.setup()
