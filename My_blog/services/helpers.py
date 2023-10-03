import datetime
from base64 import b32encode
from hashlib import sha1
from random import randint, random
import uuid
from unique_upload import unique_upload


def dateNow():
    return datetime.datetime.now() + datetime.timedelta(hours=2)


def pkgen():
    return b32encode(sha1(str(random())).digest()).lower()[:12]


def rand_int_4digits():
    return randint(1000, 9999)


def file_upload(folder_name, instance, filename):
    return "%s/%s" % (folder_name, unique_upload(instance, filename))


def get_unique_string():
    return uuid.uuid4().hex
