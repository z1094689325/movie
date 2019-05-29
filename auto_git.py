# -*- coding: utf-8 -*-

import os
import sys

os.system('git add .')

os.system('git commit -m "{}"'.format(sys.argv[1]))

os.system('git push https://gitee.com/zhangpengju/movie_resource_station_search master')



