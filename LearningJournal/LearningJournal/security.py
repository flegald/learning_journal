# coding -*- utf-8 -*-
"""Add the login and access functionality."""
from passlib.hash import sha512_crypt
import os


USERS = {'david': os.environ.get('AUTH_PW', "nothing")}
GROUPS = {'david': ['group:editors']}


def check_pw(userid, pw):
    """See if user is is in USERS."""
    if userid in USERS:
        return sha512_crypt.verify(pw, USERS[userid])


def groupfinder(userid, request):
    """Check to see if user is in USERS."""
    if userid in USERS:
        return GROUPS.get(userid, [])
