import sys, os, time, datetime, smtplib, urlparse, random, requests, json
from flask import current_app, Blueprint, render_template, abort, request, flash, redirect, url_for
#from flask.ext.login import (current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required)
# from auth.User import User

static_dev_server = Blueprint('static_dev_server', __name__,url_prefix='')


@static_dev_server.route('/static/<filename>', methods=['GET'])
def static(filename):

    static_dev_server.static_folder='static'
    return static_dev_server.send_static_file(filename)



@static_dev_server.route('/static/<depth1>/<filename>', methods=['GET'])
def static2(filename,depth1):

    print('/static/%s/%s'%(depth1,filename))
    

    static_dev_server.static_folder='static/'+depth1
    return static_dev_server.send_static_file(filename)


@static_dev_server.route('/static/<depth1>/<depth2>/<filename>', methods=['GET'])
def static3(filename,depth1,depth2):

    static_dev_server.static_folder='static/'+depth1+'/'+depth2
    return static_dev_server.send_static_file(filename)


@static_dev_server.route('/static/<depth1>/<depth2>/<depth3>/<filename>', methods=['GET'])
def static4(filename,depth1,depth2,depth3):

    static_dev_server.static_folder='static/'+depth1+'/'+depth2+'/'+depth3
    return static_dev_server.send_static_file(filename)


@static_dev_server.route('/static/<depth1>/<depth2>/<depth3>/<depth4>/<filename>/', methods=['GET'])
def static5(filename,depth1,depth2,depth3,depth4):

    static_dev_server.static_folder='static/'+depth1+'/'+depth2+'/'+depth3+'/'+depth4
    return static_dev_server.send_static_file(filename)


