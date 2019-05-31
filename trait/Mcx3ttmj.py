# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from spider import Spider


class S3ttmj:
    
    '''
    def get_film_info(self, url, encoding = None): 
        
        传入一个电影详情链接，清洗该链接数据
        
    def film_search(self, keyword, encoding = None):
        
        传入一个关键字，返回关键字的在网站的搜索结果
        
    def get_show_page_info(self,url):
        
        传入一个show_page_url返回所有电影信息
        
    def get_all_show_page_url(self):
        
        获取网站所有的show_page_url
        
    def get_all_show_page_url_yield(self):
        
        获取网站所有的show_page_url的迭代器
        
    
    
    '''
    
    domain = 'http://3ttmj.com/'
    
    
    def split_info(self, info_str):#一个用在清洗数据的方法
        
        if '/' in info_str:#表示导演用/分割开来
            
            info_str = info_str.split('/')
            
        elif ',' in info_str:
            
            info_str = info_str.split(',')
            
        elif ' ' in info_str:
            
            info_str = info_str.split(' ')
            
        else:
            
            info_str = [info_str]
            
        return [i.strip() for i in info_str if i != '']
        
        
    
    def get_film_info(self, url, encoding = None):
        
        
        regex = dict(
                ########剧情介绍
                intro = '<div class="info-desc uk-float-left uk-margin-top">\s+?<h3 class="uk-h3">.*?</h3>\s+?<p>(.*?)</p>\s+?</div>',
                
                name = '<h1>(.*?)</h1>',
                
                info = '\
<li><span>分类：</span>(.*?)</li>\s+?\
<li><span>导演：</span>(.*?)</li>\s+?\
<!-- <li><span>编剧：</span>(.*?)</li> -->\s+?\
<li><span>主演：</span><a href="(.*?)" target="_blank">(.*?)</a> <a href="(.*?)" target="_blank">(.*?)</a> <a href="(.*?)" target="_blank">(.*?)</a> <a href="(.*?)" target="_blank">(.*?)</a></li>\s+?\
<li><span>语言：</span>(.*?)</li>\s+?\
<li><span>地区：</span>(.*?)</li>\s+?\
<li><span>集数：</span>(.*?)</li>\s+?\
<li><span>上映年代：</span>(.*?)</li>\s+?\
<li><span>最后更新：</span>(.*?)</li>\s+?\
<li><span>豆瓣评分：</span>(.*?)</li>\s+?\
',

                show_list = '<li><label><input type="checkbox" class="uk-display-inline" name="choice" checked><b>(.*?)</b><a href="(.*?)" target="_blank" class="uk-display-inline uk-margin-left">(.*?)</a></label></li>',
                

                )
        info = Spider().get_info(url,encoding = encoding , **regex)
        
#        return info
        #类型
        types = self.split_info(info['info'][0][0])
#       导演  
        director = self.split_info(info['info'][0][1])
#       编剧
        Screenwriter = self.split_info(info['info'][0][2])
#       主演链接
        performer_url = [i for i in info['info'][0] if i.startswith('/?s=')]
#       主演
        performer = [i for i in info['info'][0][4:-6] if not i.startswith('/?s=')]
#       语言
        language = self.split_info(info['info'][0][-6])
#        地区
        region = self.split_info(info['info'][0][-5])
#        更新集数
        drama_series = self.split_info(info['info'][0][-4])
#        上映年代
        show_time = self.split_info(info['info'][0][-3])
#        更新时间
        update_time = self.split_info(info['info'][0][-2])
#        豆瓣评分
        score = self.split_info(info['info'][0][-1])
        
#        电影链接
        m3u8_list = [url[2] for url in info['show_list'][0:30]]
#        
#        yun_list = [url.split('$')  for url in info['show_list'] if not url.endswith('.m3u8')]
#        
#    
        film_info = dict(
#                电影名称
                name = info['name'][0],
                
                types = types,
                
                director = director,
                
                Screenwriter = Screenwriter,
                
                performer_url = performer_url,
                
                performer = performer,
                
                language = language,
                
                region = region,
                
                drama_series = drama_series,
                
                show_time = show_time,
                
                #plays = info['info'][0][9],
                
                update_time = update_time,
                
                score =score,
                
                m3u8_list = m3u8_list
                
                )
        
        
        return film_info
    
    
    def film_search(self, keyword, encoding = None):
        
        post_url = 'http://3ttmj.com/index.php?s=vod-search'
        
        data = {
                'wd': keyword,
                'submit': 'search',
                
                }
        
        regex = dict(
                
                info = '<span class="tag_1"><a href="(.*?)" target="_blank">(.*?)</a></span>\s+?\
                        <span class="tag_2">(.*?)</span>\s+?\
                        <span class="tag_3"><a href=".*?" target="_blank">(.*?)</a></span>\s+?\
                        <span class="tag_4"><a href=".*?" target="_blank">点击进入</a></span>\s+?\
                        <span class="tag_5">(.*?)</span>'
                )
        
        info = Spider().post_info(post_url, data, encoding, **regex)['info']
        
#        return info
        
        joint_url = self.domain
        
        info = [{'url':joint_url + url[1:], 'name':name, 'types':types, 'update_time': update_time} for url, name, types, update_time in info]
        
        return {'search_list': info, 'search_word': keyword, 'host': self.domain}
    
    
    def get_show_page_info(self,url):
        

        
        regex = dict(
                
                info = '\
<span class="tag_1"><a href="(.*?)" target="_blank">(.*?)</a></span>\s+?\
<span class="tag_2">(.*?)</span>\s+?\
<span class="tag_3"><a href=".*?" target="_blank">(.*?)</a></span>\s+?\
<span class="tag_4"><a href=".*?" target="_blank">点击进入</a></span>\s+?\
<span class="tag_5">(.*?)</span>'
                
#                area = '\
#                    <span class="tag_2">(.*?)</span>' ,
#                    
#                types = '\
#                    <span class="tag_3"><a href=".*?" target="_blank">(.*?)</a></span>',    
#                    
#                update_time = '\
#                    <span class="tag_5">(.*?)</span>',
                    
                )
        
        regex = Spider().get_info(url,encoding = 'utf-8',  **regex)
        
        info = [dict(url = i[0], name = i[1].split('&nbsp;')[0] ,area = i[2] , types = i[3] , update_time = i[4]) for i in regex['info']]
        
        return {'frist_info':info}

        
        
        
    
    def get_all_show_page_url(self):
        
        '''
        return:获取 https://www.subo8988.com/ 网站所有 show_page_url
        
        '''
        
        url = 'http://3ttmj.com/?s=Home-Index-index-p-{}.html'
        
        self.queue = [url.format(i) for i in range(1, 450)]
        
        
        return self.queue

    
    
    def get_all_show_page_url_yield(self):

        url = 'http://3ttmj.com/?s=Home-Index-index-p-{}.html'

        for i in range(1, 450):

            yield url.format(i)
                
    
        
if __name__ == '__main__':
    
#    url = 'http://3ttmj.com/?s=Home-Index-index-p-1.html'
    
    url = 'http://3ttmj.com/?s=Home-vod-read-id-19867.html'
    
    x = S3ttmj()
    
    #info = x.get_film_info(url)
#    info = x.film_search('射雕英雄传')
    
#a = (1,2,3,4,5,6,8,9,9,0,9,7,5,6,7,8,9)
#b = a[4:-7]
        


