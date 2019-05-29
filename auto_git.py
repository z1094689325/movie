# -*- coding: utf-8 -*-

import os
import sys


def auto_git(m):

    os.system('git add .')

    os.system('git commit -m "{}"'.format(m))

    os.system('git push https://gitee.com/zhangpengju/movie_resource_station_search master')


if __name__ == "__main__":

    auto_git(sys.argv[1])



