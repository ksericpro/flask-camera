import bson
import datetime
import os
import json
import re
import random
import string
import shutil
from cryptography.fernet import Fernet, MultiFernet

REGEX_SANITIZE_PATTERN = r'[<,>,\',\",(,),;,%]'
REGEX_SANITIZE_REPLACE_CHARACTER = '*'
SHA_KEY_1 = 'Fk3sC6DHjxpSbm1rkyeNgPdbojtzvNUB9JaV-Vlfmrc='

def conv(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()
    if isinstance(o, bson.objectid.ObjectId):
        return o.__str__()


def massageJson(messagedata):
    messagedata = messagedata.replace('u\'', '\'')
    messagedata = messagedata.replace('\'', '"')
    return messagedata


def is_json(myjson):
    try:
        json_object = json.loads(myjson)
        return json_object
    except ValueError as e:
        return None

def load_file(filename):
    if os.path.exists(filename):
        f = open(filename, "r")
        contents = f.read()
        f.close()
        return contents
    else:
        print(filename + " does not exists.")
        return ""


def is_sanitized(statement):
    if re.search(REGEX_SANITIZE_PATTERN, statement):
        return False
    else:
        return True


def sanitize_content(content):
    return re.sub(REGEX_SANITIZE_PATTERN, REGEX_SANITIZE_REPLACE_CHARACTER, content)


def sanitize_dict(data, n_list):
    n_data = {}
    print(data)
    for key, value in data.items():
        # print("key: {} | value: {}".format(key, value))
        if len(n_list) == 0:
            n_data[key] = sanitize_content(value)
        else:
            if key in n_list:
                n_data[key] = sanitize_content(value)
            else:
                n_data[key] = value
    return n_data

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def shortened_string(message, l):
    if len(message)<= l:
        info = str(message)
        return info
    info = message[:l] + (message[l:] and '..')
    return info

def copy_folder(src_dir, target_dir):
    try:
        if os.path.exists(src_dir):
            shutil.copytree(src_dir, target_dir)
    except OSError as e:
        print("Error: %s : %s" % (src_dir, e.strerror))

def remove_folder(src_dir):
    try:
        if os.path.exists(src_dir):
            shutil.rmtree(src_dir)
    except OSError as e:
        print("Error: %s : %s" % (src_dir, e.strerror))

def mv_folder(src_dir, target_dir):
    try:
        if os.path.exists(src_dir):
            shutil.move(src_dir, target_dir)
    except OSError as e:
        print("Error: %s : %s" % (src_dir, e.strerror))

def remove_file(file_path):
    try:
        os.unlink(file_path)
    except OSError as e:
        print("Error: %s : %s" % (file_path, e.strerror))

def copy_file(src_path, dest_path):
    try:
        shutil.copyfile(src_path, dest_path)
    except OSError as e:
        print("Error: %s" % e.strerror)

def encrypt_sha(message):
    f = Fernet(SHA_KEY_1)
    if isinstance(message, str):
        message = str.encode(message)
    return f.encrypt(message)

def decrypt_sha(payload):
    f = Fernet(SHA_KEY_1)
    if isinstance(payload, str):
        payload = str.encode(payload)
    return (f.decrypt(payload)).decode("utf-8") 

def get_image_uri(id, filename):
    return '/blacklist_i?id=' + id + '&filename=' + filename

def get_index_positions_by_condition(list_of_elems, condition):
    ''' Returns the indexes of items in the list that returns True when passed
    to condition() '''
    index_pos_list = []
    for i in range(len(list_of_elems)):
        if condition(list_of_elems[i]) == True:
            index_pos_list.append(i)
    return index_pos_list