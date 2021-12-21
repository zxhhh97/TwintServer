from flask import Flask
from flask import render_template, redirect,url_for
from flask import request,session
import os, inspect, logging, functools

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
