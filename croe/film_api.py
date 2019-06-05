# -*- coding: utf-8 -*-
"""
Created on Fri May 31 09:28:58 2019

@author: Administrator
"""
import trait
import redis
import queue
import threading
import json
import sys

from script_trait import TraitAPI

trait_info_dict = TraitAPI().trait_obj()

trait_info = trait_info_dict.values()#将所有特征函数的类生成列表

class FilmApi:
    
    def __init__(self):
    
        
        pool = redis.ConnectionPool(host = '192.168.2.108', port = 6379, password = '1', db = 9, decode_responses = True)
        
        self.r = redis.StrictRedis(connection_pool=pool)
        
        self.q = queue.Queue(5)#创建一个队列对象，queue.LifoQueue,创建一个堆栈，还有一个优先级队列
        
        self.search_info = {}
    

    def producer(self):#把所有特征函数的类放到到queue对象中
        
        for i in trait_info:
                  
            self.q.put(i)
            
    def consumer(self, keyword):#一个do_work函数，获取一个类，进行搜索将搜索结果放到self.search_info中
        
        while True:
            
            task = self.q.get()
            
            if task == None:
                    
                break
            
            task_class = task()
            
            
            try:
            
                info = task_class.film_search(keyword)
                
            except:
                #raise
                
                self.q.task_done()
                
                print(task_class.domain, '失败')
                
            else:
            
                self.search_info[task_class.domain] = info
                
                print(task_class.domain, '完成')
                
                self.q.task_done()
                

        
    def my_thread(self, keyword):#运行线程的main函数
        

        
        if self.r.exists(keyword):#如果在redies里有缓存就直接从redis里取出来，
            
            print(keyword, '搜索结果在redis里有')
            
            return json.loads(self.r.get(keyword))
        

        threads = []
        
        for i in range(len(trait_info)):#有几个类对象就开启几个线程
        
            t = threading.Thread(target = self.consumer, args = (keyword,))
            
            t.start()
            
            threads.append(t)
            
        
        self.producer()                 #往任务队列添加任务
        
        
        self.q.join()                   #阻塞主线程直到所有的队列任务完成
        print('卡q’')
        for i in range(len(trait_info)):#退出线程机制

            print('******************')
            
            self.q.put(None)
            
        print('ka qq')
            
            
        for t in threads:
            
            t.join()
            
            
        self.r.set(keyword, json.dumps(self.search_info), ex = 6*60*60)   #保存到redis中，6个小后过期
            
            
        
        return self.search_info
    
    
    def search_detail(self, keyword):
        
        if self.r.exists(keyword+'_detail'):
            
            print(keyword, '详细的搜索结果在redis里有')
            
            return json.loads(self.r.get(keyword+'_detail'))
                       
        
        search_info = self.my_thread(keyword)
        
        detail_info = {'keyword': keyword}
        
        
        for host, info in search_info.items():
            
            search_list = info['search_list'][:3]
            
            if search_list:#如果search_list为空则跳过
                
                detail_list = []
                
                for i in search_list:
                    
                    url = i['url']  #获取视频url
                    
                    trait_class = trait_info_dict[host]#获取对应的class
                    
                    try:
                    
                        film_info = trait_class().get_film_info(url)#获取url对应的信息
                        
                        
                        
                    except:
                        
                        
                        
                        
                        print(trait_class, '报错',str(sys.exc_info()))
                        print(url)
                        
                    else:
                    
                        detail_list.append(film_info)#将作息放入到列表中
                    
                detail_info[host] = detail_list#将这个网站的搜索信息放入到detail_info中
                
        self.r.set(keyword+'_detail', json.dumps(detail_info), ex = 6*60*60)
        
        
        return detail_info
            
                           
            
        
        
if __name__ == '__main__':
    
    
    x= FilmApi()
    
    r = x.r
    
    def clear_redis():
        
        for i in r.keys():
            
            r.delete(i)

    clear_redis()
            
            
    info = x.search_detail('筑梦情缘')
    #
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
