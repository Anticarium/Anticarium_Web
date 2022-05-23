#!/usr/bin/python3

import logging
import sys
import os

logging.basicConfig(stream=sys.stderr)

ANTICARIUM_WEB_PATH = os.environ["ANTICARIUM_WEB_PATH"]
if not ANTICARIUM_WEB_PATH:
    raise RuntimeError("ANTICARIUM_WEB_PATH environment variable not defined!")

if not os.environ["ANTICARIUM_SERVER_IP"]:
    raise RuntimeError("ANTICARIUM_SERVER_IP environment variable not defined!")

# Otherwise flask module cannot be found. This is not a perfect solution and requires
# Python virtual environment for mod-wsgi as a real solution. Maybe this path to PATH
# will also work
sys.path.insert(0, f"/home/pi/.local/lib/python3.9/site-packages")

sys.path.insert(0, f"{ANTICARIUM_WEB_PATH}")

from anticarium_web import app as application
