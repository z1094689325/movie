from django.shortcuts import render

from django.http import HttpResponse, JsonResponse

from croe.film_api import FilmApi

import json

# Create your views here.


def index(request):

    return render(request, 'film_search/index.html')


def search_get(request):

    keyword = request.GET.get('keyword')

    print(keyword)

    search_info = FilmApi().my_thread(keyword)

    return HttpResponse(str(search_info))

    return render(request, 'film_search/search-list.html')




    
