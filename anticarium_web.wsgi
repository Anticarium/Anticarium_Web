#! /usr/bin/python3

import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/home/pi/Desktop/Anticarium_Web/Anticarium_Web')
from anticarium_web import app as application
application.secret_key = 'anything you wish'

