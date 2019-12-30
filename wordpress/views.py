import requests
from django.shortcuts import render

target = 'https://rifondazionepodistica.it/wp-json/wp/v2/'

def wp_list_view(request):
    if 'page' in request.GET:
        page = int(request.GET['page'])
    else:
        page = 1
    filter = {
        '_fields': 'id,title,excerpt,jetpack_featured_media_url',
        'per_page': 9,
        'page': page,
        }
    response = requests.get(target + 'posts', params = filter )
    wp_posts = response.json()
    posts = []
    for wp_post in wp_posts:
        post = {}
        post['id'] = wp_post['id']
        post['title'] = wp_post['title']['rendered']
        post['excerpt'] = wp_post['excerpt']['rendered']
        if wp_post['excerpt']['protected'] == 'true':
            post['visible'] = False
        else:
            post['visible'] = True
        post['image'] = wp_post['jetpack_featured_media_url']
        posts.append(post)
    return render(request, 'wordpress/wp_list.html', {'posts': posts, 'page': page,
    'previous': page-1, 'next': page+1
    })
