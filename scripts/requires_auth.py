from functools import wraps
from flask import request, Response
import os
import json

def authentication_enabled():
    return True

def disable_authentication():
    raise Exception('authentication cannot be disabled')

def set_authentication(username, password):
    raise Exception('unimplemented')

def check_auth(username, password, role):
    """This function is called to check if a username /
    password combination is valid.
    """
    with open('scripts/users.json') as data_file:
        data = json.load(data_file)
        authentication = username in data['users'] and password == data['users'][username]['password']
        return authentication and role in data['users'][username]['roles']

    return False

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="docker-compose-ui"'})


def requires_auth(method_or_name):
    """Check authentication and authorization"""
    def decorator(method):
        if callable(method_or_name):
            method.gw_method = method.__name__
        else:
            method.gw_method = method_or_name
        @wraps(method)
        def wrapper(*args, **kwargs):
            if isinstance(method_or_name, basestring):
                role = method_or_name
            else:
                role = None
            auth = request.authorization
            if auth and check_auth(auth.username, auth.password, role):
                return method(*args, **kwargs)
            return authenticate()
        return wrapper
    if callable(method_or_name):
        return decorator(method_or_name)
    return decorator