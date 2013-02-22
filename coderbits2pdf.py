#!/usr/bin/env python

"""
Coderbits2PDF - Convert your coderbits profile to pdf.
Added option of adding your github repos.

Usage -
python coderbits2pdf --make username      # create resume
python coderbits2pdf --add username       # add user
python coderbits2pdf --del username       # delete user
python coderbits2pdf --add-repo username  # add more repositories
python coderbits2pdf --del-repo username  # delete repositories
"""

__author__= 'elssar <elssar@altrawcode.com>'
__license__= 'MIT'

from requests import post, get
from json import loads
from weasyprint import HTML, CSS
from jinja2 import Template
from os import path
from sys import argv
from yaml import dump, safe_load as load
from logging import getLogger

logger= getLogger('weasyprint')
logger.handlers= []                # Shut up weesyprints noisy logger

dir= path.dirname(path.abspath(__file__))
coderbits= 'https://coderbits.com/{0}.json'
github= 'https://api.github.com/users/{0}/repos'
charts= 'http://{0}.chart.apis.google.com/chart?'
header= {'user-agent': 'coderbits2pdf'}

def get_coderbits(username):
    profile= get(coderbits.format(username))
    if profile.status_code!=200 or profile.headers['content-length']=='2':
        return None
    return loads(profile.content)

def get_repos(username, selected_repos=None):
    req= get(github.format(username), headers= header)
    repos= loads(req.content)
    if selected_repos is None:
        return repos
    contents= []
    for repo in selected_repos:
        if repo in repos:
            contents.append(repos[repo])
        else:
            print 'Warning! Repository {0} not found in github.'.format(repo)
    return contents

def get_chart_url(data, name, labels):
    payload= {'cht': 'p3',
            'chs': '300x150',
            'chco': '2F69BF|A2BF2F|BF5A2F|BFA22F|772FBF',
            'chtt': name,
            'chd': 't:'+','.join(data),
            'chdl': '|'.join(labels)
            }
    query_string= ''
    for key in payload:
        query_string+= '{0}={1}&'.format(key, payload[key])
    return query_string[:-1]

def save_pdf(html, output, css):
    HTML(string=html).write_pdf(output, stylesheets=[CSS(css)])

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
    coderbits= get_coderbits(username)
    img_urls= []
    i= 0
    for entry in coderbits:
        if 'top_' in entry:
            data= []
            labels= []
            for value in coderbits[entry]:
                data.append(float(value['count']))
                labels.append(value['name'])
            total= sum(data)
            data= map(lambda x: str((x/total)*100), data)
            labels= ['{0} {1}%'.format(x, y[:y.find('.')+3]) for x, y in zip(labels, data)]
            title= entry.replace('_', ' ')
            title= title.title()
            query_string= get_chart_url(data, title, labels)
            img_urls.append(charts.format(i)+query_string)
            i+= 1
    args= []
    args.append(config[username]['github'])
    args.append(config[username]['repositories'] if len(config[username]['repositories'])>0 else None)
    github= get_repos(*args)
    try:
        with open(path.join(dir, 'layout.html'), 'r') as f:
            layout= f.read()
    except IOError:
        print 'Template not found!'
        return
    template= Template(layout)
    html= template.render(username=username, coderbits=coderbits, github=github, img_urls=img_urls, email=config[username]['email'])
    save_pdf(html, path.join(dir, 'resume.pdf'), path.join(dir, 'bootstrap.css'))

def add_user(username):
    try:
        with open(path.join(dir, 'config.yaml'), 'r') as con_file:
            config= load(con_file.read())
    except IOError:
        config= {}
    email= raw_input("Enter email: ")
    github= raw_input("Enter github username: ")
    config[username]= {'email': email, 'github': github, 'repositories': []}
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
    args= {'--add': add_user,
        '--del': del_user,
        '--add-repo': add_repos,
        '--del-repo': del_repos,
        '--make': create_resume
        }
    if argv[1] not in args or len(argv)!=3:
        print 'Invalid arguments!'
        print __doc__
        return
    args[argv[1]](argv[2])

if __name__=='__main__':
    main()
