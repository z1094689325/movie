

from django.shortcuts import render

from django.http import HttpResponse, JsonResponse

from croe.film_api import FilmApi

import json



# Create your views here.


def index(request):

    context = {}

    return render(request, 'film_search/index.html',context)


def search_get(request):

    keyword = request.GET.get('keyword')



    search_info = FilmApi().search_detail(keyword)

    count_search_info = 0

    for key, value in search_info['search_detail'].items():

        count_search_info += len(value)
        

    search_info.update({'count': count_search_info})


    context = search_info

    '''
        {'keyword':xx, 'search_detail':{host:{}}}
    '''


    return render(request, 'film_search/search-list.html', context)

def play(request):

    'search/play/?url=http://123ku.com/?m=vod-detail-id-17268.html'

    url = request.GET.get('url')
    
    num = request.GET.get('num')
    print(num)
    
    if num == None:
        
        num = 0
    
    detail = FilmApi().single_detail(url)
    
    detail.update({'show_now':detail['m3u8_list'][int(num)]})

    

    context = detail

    return render(request, 'film_search/play.html', context)




    
