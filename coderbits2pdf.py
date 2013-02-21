#!/usr/bin/env python

"""
Coderbits2PDF - Convert your coderbits profile to pdf.
Added option of adding your github repos.

Usage -

"""

__author__= 'elssar <elssar@altrawcode.com>'
__license__= 'MIT'

from requests import post, get
from json import loads
from xhtml2pdf.pisa import CreatePDF
from jinja2 import Template
from os import path
from sys import argv
from yaml import safe_load as load

dir= path.dirname(path.abspath(__file__))
coderbits= 'https://coderbits.com/{}.json'
github= 'https://api.github.com/users/{}/repos'
charts= 'https://chart.googleapis.com/'

def main():
    pass

if __name__=='__main__':
    main()