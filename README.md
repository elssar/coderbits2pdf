coderbits2pdf
=============

Create a pdf of your [Coderbits](https://coderbits.com) profile, with the option of listing any of your github repos.

Usage -

    python coderbits2pdf --make username    # create resume
    python coderbits2pdf --add username       # add user
    python coderbits2pdf --del username       # delete user
    python coderbits2pdf --add-repo username  # add more repositories
    python coderbits2pdf --del-repo username  # delete repositories

Requires -

 - [requests](http://docs.python-requests.org/en/latest/index.html)
 - [PyYaml](http://pyyaml.org/)
 - [xhtml2pdf](http://www.xhtml2pdf.com/)
 - [jinja2](http://jinja.pocoo.org)
