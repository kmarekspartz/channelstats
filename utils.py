#! /usr/bin/env python2.7

import collections
import decimal
import json
import re
import time

import config

# Helper class to convert a DynamoDB item to JSON.


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


def dumps(j, indent=4):
    """
    json.dumps(j), but deal with Decimal encoding
    """
    return json.dumps(j, indent=indent, cls=DecimalEncoder)


def dump(j):
    """
    json.dump(j), but deal with Decimal encoding
    """
    j = dumps(j)
    return json.loads(j)


def prune_empty(row):
    """
    prune attributes whose value is None
    """
    new_row = {}
    for k in row:
        if row[k]:
            new_row[k] = row[k]
    return new_row


def chunks(l, n):
    n = max(1, n)
    return (l[i:i + n] for i in range(0, len(l), n))


def make_ordered_dict(d):
    """
    Turn a {k:v} dictionary into an ordered dictionary ordered from largest
    v to smallest
    """
    k = list(d.keys())
    k.sort(key=lambda x: d[x])
    k.reverse()
    nd = collections.OrderedDict()
    for i in k:
        nd[i] = d[i]
    return nd


def find_user_mentions(text):
    """
    Given message text, returns what users are mentioned
    (may be empty list)
    """
    # text is of the form "whatever <@UID> and also ..."
    return [x[2:-1] for x in re.findall("<@U[A-Z0-9]+>", text)]

def rank(n):
    r = {0: 'th', 1: 'st', 2: 'nd', 3: 'rd'}
    if n in r:
        return "{}{}".format(n, r[n])
    return "{}th".format(n)

def valid_cid(cid):
    return re.match("^C[A-Z0-9]+$", cid)

def valid_uid(uid):
    return re.match("^U[A-Z0-9]+$", uid)

def make_day(ts):
    """
    Given a str ts, return yyyy-mm-dd
    """
    lt = time.localtime(int(float(ts)))
    return time.strftime("%Y-%m-%d", lt)

def today():
    lt = time.localtime(time.time())
    return time.strftime("%Y-%m-%d", lt)

def save(blob, fname):
    if type(blob) == str:
        f = open(fname, "w")
    else:
        f = open(fname, "wb")
    f.write(blob)
    f.close()

def make_url(cid, ts):
    """
    Return a URL for the message specified
    """
    return "https://{}.slack.com/archives/{}/p{}".format(config.slack_name, cid, ts.replace(".", ""))

