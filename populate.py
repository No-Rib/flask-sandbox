#!.venv/bin/python
"""
Customizable script for populating the project.
"""

import argparse
import random
import string
import sys

from app import db
from app.models import PostModel, UserModel

DEFAULT_PASSWORD_LENGTH = 30
DEFAULT_POST_BODY_LENGTH = 200
DEFAULT_POST_HEADER_LENGTH = 50
DEFAULT_USERNAME_LENGTH = 15


def generate_string(string_length):
    """Generated random string of given length."""

    return "".join(
        random.choice(string.ascii_letters + string.digits) for _ in xrange(string_length)
    )


parser = argparse.ArgumentParser()

parser.add_argument(
    "-u, --users",
    default=100,
    dest="users",
    help="number of users to generate",
    metavar="N_OF_USERS",
    type=int,
)

parser.add_argument(
    "-p", "--posts",
    default=100,
    dest="posts",
    help="number of posts per user to generate",
    metavar="N_OF_POSTS",
    type=int,
)

args = parser.parse_args()

try:
    for user_i in xrange(args.users):
        try:
            username = generate_string(DEFAULT_USERNAME_LENGTH)
            password = generate_string(DEFAULT_PASSWORD_LENGTH)
            email = "{0}@fakedomain.com".format(username)

            fake_user = UserModel(username=username, password=password, email=email)
            db.session.add(fake_user)
            db.session.commit()

            for post_i in xrange(args.posts):
                post_header = generate_string(DEFAULT_POST_HEADER_LENGTH)
                post_body = generate_string(DEFAULT_POST_BODY_LENGTH)

                fake_post = PostModel(
                    header=post_header, body=post_body, username=username, user_id=fake_user.id)
                db.session.add(fake_post)

            db.session.commit()
        except BaseException as e:
            print "Failed to create user {0}: {1}".format(user_i, e)
except BaseException as e:
    sys.exit("Population of db failed: {0}".format(e))

print "Db was successfully populated."
