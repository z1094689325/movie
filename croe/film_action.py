# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import sqlite3
import threading
import sys
import json


import redis






class FilmAction():
    
    '''
    def test_db(self):
        
        测试数据库是否存在，不存在新建
        
    def work(self):
        
        将网站所有电影信息写入数据库中
    def my_thread(self):
        
        开启多条线程将写入数据库中
        
        
    
    
    
    '''
    
    def __init__(self, film_object):
        
        self.film_object = film_object
        
        self.r = redis.StrictRedis(host = '192.168.2.107', port = '6379', password = '1', db = '5', decode_responses = True)
        
        self.conn = sqlite3.connect('film.sqlite3', check_same_thread = False)
        
        self.cursor = self.conn.cursor()
        
        self.cursor_lock = threading.Lock()
        
        self.test_db()
        
        self.iter_show_page_url = self.film_object.get_all_show_page_url_yield()
        
        
    ######特征函数#######
    
    def test_db(self):
              
        creart_sql = '''\
        
            CREATE TABLE IF NOT EXISTS film_info(
            
            
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    
                    name TEXT,
                    
                    url  TEXT UNIQUE,
                    
                    update_time  TEXT,
                    
                    types  TEXT,
                    
                    status TEXT NULL
            
            
            )
        
        '''
        
        
        self.cursor_lock.acquire()
        
        self.cursor.execute(creart_sql)
        self.conn.commit()
        
        self.cursor_lock.release()
      
            
    def work(self):
        
        insert_sql = '''
        
            INSERT INTO film_info
            
            (name ,url, update_time, types)   
            
            VALUES       
            
            (?, ?, ?, ?)'''
        
        
        while True:
         
            show_page_url = next(self.film_object.iter_show_page_url)
            
            try:
            
                info = self.film_object.get_show_page_info(show_page_url)['film_list']
                
            except:
                
                self.redis.set(show_page_url, str(sys.exc_info()))
                
                print('出错啦', show_page_url)
                
            else:
                
      
                insert_list = [(i['name'], i['url'], i['update_time'], i['types']) for i in info]
                
                self.cursor_lock.acquire()
                    
                try:
                    
                    self.cursor.executemany(insert_sql, insert_list)
                    
                except sqlite3.IntegrityError:
                    
                    print(show_page_url, '已经存在')
                    
                    self.cursor_lock.release()
                    
                else:
                    
                    self.conn.commit()
                    
                    print(show_page_url)
                      
                    self.cursor_lock.release()
                
                
            
    def my_thread(self):
        
        for i in range(5):
        
            t = threading.Thread(target = self.work)#, args = (), kwargs = {})
            
            t.start()
            
            
    def search_detail(self, keyword, page = None):
        
        if page == None:
            
            page = 0
        
        search_info = self.film_object.film_search(keyword)['search_list'][page * 5 : (page+1)*5]
        
        #detail_search_list = [self.film_object.get_film_info(i['url'])  for i in search_info]
        
        detail_search_list = []
        
        def run(url):
            
            detail_search_list.append(self.film_object.get_film_info(url))
        
        
        threads = []
        
        for i in range(5):
            
            try:
            
                url = search_info.pop()['url']
                
            except IndexError:
                
                print('search_detail, 任务队列完成')
                
                break
                
            else:
            
            
        
                t = threading.Thread(target = run, args = (url,))
                
                threads.append(t)
                
                t.start()
                
        for t in threads:
                
            t.join()
            
            
            
        self.r.set(keyword, json.dumps({'info' :detail_search_list}))
        
        
        #self.r.hmset(keyword,{'info' :detail_search_list})
            
               
        return {'info' :detail_search_list}
    
    
    def search_detail_redis(self, keyword):
        
        if self.r.exists(keyword):
            
            return json.loads(self.r.get(keyword))
        
            #self.r.hget(keyword)
        else: 
            
            return self.search_detail()
            
            
            
            
        
    
    
    
if __name__ == '__main__':
    
    from FilmSubo8988 import FilmSubo8988
    
    x = FilmAction(FilmSubo8988())
    
    #info = x.search_detail('我只喜欢你')
    
    
    
        
        
        
        
        
        
        
        
            
            
        
    
    
    
        
        


