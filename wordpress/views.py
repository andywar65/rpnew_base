import requests
from django.shortcuts import render

target = 'https://rifondazionepodistica.it/wp-json/wp/v2/'

def wp_list_view(request):
    response = requests.get(target + 'posts?per_page=1')
    posts = response.json()
    title = posts[0]['title']['rendered']
    return render(request, 'wordpress/list.html', {'title': title,
    })
