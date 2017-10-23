# -*- coding: utf-8 -*-
__author__ = 'Eggsy'
__date__ = '2017/10/23 20:00'


from scrapy.cmdline import execute

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(['scrapy', 'crawl', 'jobbole'])
