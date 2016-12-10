import sys, os, time, datetime, smtplib, urlparse, random, requests, json
from flask import current_app, Blueprint, render_template, abort, request, flash, redirect, url_for
#from flask.ext.login import (current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required)
# from auth.User import User

static_dev_server = Blueprint('static_dev_server', __name__,url_prefix='')


@static_dev_server.route('/_static/<filename>', methods=['GET'])
def static(filename):

    static_dev_server.static_folder='_static'
    return static_dev_server.send_static_file(filename)



@static_dev_server.route('/_static/<part1>/<filename>', methods=['GET'])
def static2(filename,part1):

    print('/_static/%s/%s'%(part1,filename))
    

    static_dev_server.static_folder='_static/'+part1
    return static_dev_server.send_static_file(filename)


@static_dev_server.route('/_static/<part1>/<part2>/<filename>', methods=['GET'])
def static3(filename,part1,part2):

    static_dev_server.static_folder='_static/'+part1+'/'+part2
    return static_dev_server.send_static_file(filename)


@static_dev_server.route('/_static/<part1>/<part2>/<part3>/<filename>', methods=['GET'])
def static4(filename,part1,part2,part3):

    static_dev_server.static_folder='_static/'+part1+'/'+part2+'/'+part3
    return static_dev_server.send_static_file(filename)


@static_dev_server.route('/_static/<part1>/<part2>/<part3>/<part4>/<filename>/', methods=['GET'])
def static5(filename,part1,part2,part3,part4):

    static_dev_server.static_folder='_static/'+part1+'/'+part2+'/'+part3+'/'+part4
    return static_dev_server.send_static_file(filename)


