# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 10:31:32 2019

@author: Administrator
"""
import multiprocessing
import importlib
import threading
import sys
sys.path.append('trait')
from setting import DBConnect

from script_trait import trait_info

trait_info = trait_info()



redis_conn = DBConnect().redis_conn

class ShowPageQueue:
    
    def __init__(self):
        
        self.trait_class_list = self.take_trait_class_list()
        
#        print(self.trait_class_list)
    
    @staticmethod
    def take_trait_class_list():
               
        
        class_list = []#生成一个所有类的列表
        
        for i in trait_info:
        
            trait = importlib.import_module(i.replace('trait\\', '').replace('.py', ''))

            #trait = __import__(i.replace('trait\\', '').replace('.py', ''))#和上面的方法效果一样
        
            class_list.append(getattr(trait, trait_info[i]))
            
        return class_list
    
    @staticmethod
    
    def take_trait_class_dict():
        
        class_list = []#生成一个所有类的列表
        
        
        for i in trait_info:
        
            trait = importlib.import_module(i.replace('trait\\', '').replace('.py', ''))

            #trait = __import__(i.replace('trait\\', '').replace('.py', ''))#和上面的方法效果一样
        
            class_list.append(getattr(trait, trait_info[i]))
            
        
            
        return {i.domain: i for i in class_list}#{域名：类对象}
        
        
            
    
    def make_show_page_queue(self):
        
        while True:
            
            try:
            
                trait_class = self.trait_class_list.pop()
                
            except IndexError:
                
                
                print('任务完成')
                
                break
            
            else:   
            
                show_page_url = trait_class().get_all_show_page_url()
                
                redis_conn.rpush('show_page_url', *show_page_url)
                
                print(trait_class.domain, '加队队列')
            
    def threads_make_show_page_queue(self):
        
        for i in range(len(trait_info)):
            
#            t = multiprocessing.process(target = self.make_show_page_queue)    #
        
            t = threading.Thread(target = self.make_show_page_queue)
            t.start()
            
if __name__ == '__main__':
    
    x = ShowPageQueue()
    
    #
    
            
            
        
        
        
        
        
        
        
        
        
        



