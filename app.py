from load import init
from flask import Flask, render_template, request

import re
import sys
import os

corrector, model, params = init()
