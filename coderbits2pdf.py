#!/usr/bin/env python

"""
Coderbits2PDF - Convert your coderbits profile to pdf.
Added option of adding your github repos.

Usage -

"""

__author__= 'elssar <elssar@altrawcode.com>'
__license__= 'MIT'

from requests import post
from json import loads
from xhtml2pdf.pisa import CreatePDF
from jinja2 import Template
from os import path
from sys import argv

dir= path.dirname(path.abspath(__file__))
config= {}

try:
    with open(dir+'/config.txt', 'r') as confile:
        for line in confile:
            value= line.split()
            config[value[0]]= value[1]
except IOError:
    print "Warning! Configuration could not be loaded"
    print "Reverting to defaults"
    config['template']= 'layout.css'
    config['css']= 'style.css'
    config['output']= 'resume.pdf'

