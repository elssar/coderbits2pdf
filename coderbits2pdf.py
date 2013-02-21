#!/usr/bin/env python

"""
Coderbits2PDF - Convert your coderbits profile to pdf.
Added option of adding your github repos.

Usage -
python coderbits2pdf --create username    # create resume
python coderbits2pdf --add username       # add user
python coderbits2pdf --del username       # delete user
python coderbits2pdf --add-repo username  # add more repositories
python coderbits2pdf --del-repo username  # delete repositories
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

def get_chart(data, name, labels, username):
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
    with open(path.join(dir, '{0}-{1}.png'.format(username, name)), 'wb') as f:
        f.write(image)

def save_pdf(html, output, css):
    with open(output, 'wb') as resume:
        CreatePDF(html, resume, default_css=css)

def create_resume(username):
    try:
        with open(path.join(dir, 'config.yaml'), 'r') as con_file:
            config= load(con_file)
    except IOError:
        print 'Error opening config.yaml'
        return
    if username not in config:
        print 'Error! User does not exist'
        return
    

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

def del_repos(username):
    try:
        with open(path.join(dir, 'config.yaml'), 'r') as con_file:
            config= load(con_file)
    except IOError:
        print 'Config file does not exist.'
        return
    if username not in config:
        print 'User does not exist.'
        return
    print 'Which repositories do you want to remove from the list?'
    print 'Enter the names one per line, and leave line blank when done.'
    while True:
        repo= raw_input()
        if repo=='':
            break
        if repo in config[username]['repositories']:
            config[username]['repositories'].remove(repo)
            print 'Repository {0} deleted.'.format(repo)
        else:
            print 'Error! Repository not in list.'

def add_repos(username):
    try:
        with open(path.join(dir, 'config.yaml'), 'r') as con_file:
            config= load(con_file)
    except IOError:
        print 'Config file does not exist.'
        return
    if username not in config:
        print 'User does not exist.'
        return
    print 'Which repositories do you want to add to the list?'
    print 'Enter the names one per line, and leave line blank when done.'
    while True:
        repo= raw_input()
        if repo=='':
            break
        if repo not in config[username]['repositories']:
            config[username]['repositories'].append(repo)
            print 'Repository {0} added'.format(repo)
        else:
            print 'Error! Repository already in list.'

def main():
    pass

if __name__=='__main__':
    main()