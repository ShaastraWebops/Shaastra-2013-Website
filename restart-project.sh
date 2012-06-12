#!/bin/bash
fcgi_file=~/public_html/forums.shaastra.org/django.fcgi;
pkill -9 django
touch $fcgi_file
