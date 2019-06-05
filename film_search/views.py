from django.shortcuts import render

from django.http import HttpResponse, JsonResponse

from croe.trait.FilmSubo8988 import FilmSubo8988

import json

# Create your views here.


def index(request):

    return render(request, 'film_search/index.html')
    # return HttpResponse('Hello World !!!')

def search_get(request):

    keyword = request.GET.get('keyword')

    # print(keyword)

    search_info = FilmSubo8988().film_search(keyword)

    return render(request, 'film_search/search-list.html')

    # return JsonResponse(search_info)

    # return HttpResponse(json.dumps(search_info))
    
