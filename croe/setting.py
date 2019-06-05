# -*- coding: utf-8 -*-
"""
Created on Fri May 31 09:28:58 2019

@author: Administrator
"""

from pymongo import MongoClient

import redis

#############数据库配置################

mongo_host = '192.168.2.108'

mongo_port = 27017

redis_host = '192.168.2.108'

redis_port = '6379'

redis_pswd = '1'

redis_use_db = '0'

#############################
        
class DBConnect:

    
    instance = None              # 记录第一个被创建对象的引用
    
    init_flag = False            # 记录是否执行过初始化动作



    def __new__(cls, *args, **kwargs):

        
        if cls.instance is None:      # 1. 判断类属性是否是空对象
            
            cls.instance = super().__new__(cls)      # 2. 调用父类的方法，为第一个对象分配空间

        
        return cls.instance         # 3. 返回类属性保存的对象引用

    def __init__(self):

        if not DBConnect.init_flag:
            
            #print("初始化音乐播放器")

            self.mongo_conn = MongoClient(mongo_host, int(mongo_port))


            pool = redis.ConnectionPool(host= redis_host, port=redis_port, password = redis_pswd, db = redis_use_db, decode_responses = True)


            self.redis_conn = redis.StrictRedis(connection_pool=pool)

            
            DBConnect.init_flag = True

            
        
            
        
        
if __name__ == '__main__':
    x = DBConnect()
    pass
    
    #x= FilmApi()
    #info = x.my_thread('西游记')
