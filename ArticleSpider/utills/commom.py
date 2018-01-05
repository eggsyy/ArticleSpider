# -*- coding: utf-8 -*-
__author__ = 'Eggsy'
__date__ = '2018/1/5 14:34'

import hashlib


def get_md5(url):
    if isinstance(url, unicode):
        url = url.encode('utf-8')
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()

if __name__ == '__main__':
    print get_md5('http://jobbole.com')
