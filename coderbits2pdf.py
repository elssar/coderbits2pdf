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
from yaml import dump, safe_load as load

dir= path.dirname(path.abspath(__file__))
coderbits= 'https://coderbits.com/{0}.json'
github= 'https://api.github.com/users/{0}/repos'
charts= 'https://chart.googleapis.com/'
header= {'user-agent': 'coderbits2pdf'}

def get_coderbits(username):
    profile= get(coderbits.format(username), headers= header)
    if profile.status_code!=200 or len(profile.headers['content'])==2:
        return None
    return loads(profile.content)

def get_repos(username, selected_repos=None):
    req= get(github.format(username), headers= header)
    repos= loads(req.content)
    if selected_repos is None:
        return repos
    contents= []
    for repo in repos:
        if repo['name'] in selected_repos:
            contents.append(repo)
    return contents

def get_chart(data, name, labels):
    payload= {'cht': 'p3',
            'chs': '250x150',
            'chco': '2F69BF|A2BF2F|BF5A2F|BFA22F|772FBF',
            'chtt': name,
            'chd': 't:'+','.join(data),
            'chdl': '|'.join(labels)
            }
    header['content-type': 'image/png']
    req= post(charts, headers= header, data= payload)
    image= req.content
    with open(path.join(dir, '{0}.png'.format(name)), 'wb') as f:
        f.write(image)

def create_resume(html, output, css):
    with open(output, 'wb') as resume:
        CreatePDF(html, resume, default_css=css)

def add_user(username, github):
    try:
        with open(path.join(dir, config.yaml), 'r') as con_file:
            config= load(con_file.read())
    except IOError:
        config= {}
    config[username]= {'github': github, 'repositories': []}
    print 'Do you want to specify which github repos to get?'
    print 'Enter the repository name, one per line. Enter blank line when done.'
    print 'Or leave blank if you want all github repos to be included.'
    while True:
        repo= raw_input()
        if repo=='':
            break
        config['repositories'].append(repo)
    with open(path.join(dir, 'config.yaml'), 'w') as con_file:
        dump(config, con_file)

def del_user(username):
    try:
        with open(path.join(dir, 'config.yaml'), 'r') as con_file:
            config= load(con_file.read())
    except IOError:
        print 'No config file.'
        return
    if username not in config:
        print 'User {0} does not exist.'.format(username)
        return
    del config[username]
    print 'User {0} deleted.'.format(username)

def del_repos():
    pass

def add_repos():
    pass

def main():
    pass

if __name__=='__main__':
    main()