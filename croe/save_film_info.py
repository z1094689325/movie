# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 14:40:57 2019

@author: Administrator
"""
#import os

import sys
import json
import threading
from .setting import DBConnect

from show_page_queue import ShowPageQueue


trait_dict = ShowPageQueue.take_trait_class_dict()


mongo_conn = DBConnect().mongo_conn

db = mongo_conn['film_intro']


redis_conn = DBConnect().redis_conn

class SaveFilmToMongo:
    
    def save_film_to_mongo(self, show_page_url):
        
        '''
        保存show_page_url信息到mongodb中
        
        
        '''
        
        
        
        for domin in trait_dict:#迭代现有特征函数的网站
            
            if domin in show_page_url:#确定传入的show_page_url是哪个网站
                
                obj = trait_dict[domin]()#调取对应的函数
                
                try:
                
                    info = obj.get_show_page_info(show_page_url)['film_list']#获取show_page_url内容
                    
                except:
                    
#                    os.exc_info()
                    
                    error_info = {show_page_url :str(sys.exc_info)}#如果报错暂时将错误链接和信息保存到redis里
                    
                    redis_conn.lpush('error_url', json.dumps(error_info))
                    
                else:
                    
                
                
                
                    if not info:
                        
                        redis_conn.lpush('error_url', json.dumps({show_page_url:'空值'}))
                        
                    else:     
                    
        #                for i in info:
        #                    
        #                    db.film_intro.insert_one(i)
                            
                        db.film_intro.insert_many(info)#一次插入多条，info要是列表
                
                
    def worker(self):
        
        while True:
            
            show_page_url = redis_conn.rpop('show_page_url')
            
            self.save_film_to_mongo(show_page_url)
            
            print(show_page_url, 'done')
            
            
            
            
                    

    def thread_save_film_to_mongo(self):
        
        for i in range(5):
            
            t = threading.Thread(target = self.worker)
            
            t.start()
            
            
        
    
                
                
        
        
        
        
        
        
    
    
