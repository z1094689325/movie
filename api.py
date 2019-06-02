# -*- coding: utf-8 -*-
"""
Created on Fri May 31 09:28:58 2019

@author: Administrator
"""


import os
import sys

sys.path.append('trait')

import glob

import importlib

from script_trait import trait_info


trait_info = trait_info()

class FilmApi:
    
    def film_search(self, keyword):
        
        #trait = __import__('FilmSubo8988')
        
        class_list = []
        
        for i in trait_info:
        
            trait = importlib.import_module(i.replace('trait\\', '').replace('.py', ''))
        
            class_list.append(getattr(trait, trait_info[i]))
            
        
            
        return [i().film_search(keyword) for i in class_list]
        
        

        
        
        
        
if __name__ == '__main__':
    
    x= FilmApi()
    #info = x.film_search('筑梦情缘')

    
    
