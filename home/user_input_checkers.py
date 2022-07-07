# Contains a set of functions that check user input for various purposes.

import re

def format_name(name):
    name = name.strip(' ')
    while '  ' in name:
        name = name.replace('  ', ' ')
    formated_name = []
    for ch in name:
        if ch.isalpha() or ch.isdigit() or ch in ('-', ' ', '_'):
            formated_name.append(ch)
    return ''.join(formated_name[:50])

def check_name(name):
    if len(name) < 3 or len(name) > 50:
        return False
    return True

def check_mobile(mobile):
    if len(mobile) != 10:
        return False
    if not mobile.isdigit():
        return False
    return True

def check_email(email):
    if len(email) > 50:
        return False
    if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
        return False
    return True

def check_password(password):
    if len(password) < 8:
        return False
    return True


def parse_promo(code):
    parsed = []
    for i in range(min(len(code), 50)):
        if code[i].isalpha() or code[i].isdigit():
            parsed.append(code[i])
    
    return ''.join(parsed).upper()