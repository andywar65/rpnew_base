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

def wp_detail_view(request, id):
    filter = {
        'id': id,
        '_fields': 'title,content,jetpack_featured_media_url,date,author,categories',
        }
    response = requests.get(target + 'posts/' + str(id), params = filter )
    wp_post = response.json()
    #here we have to go back and fetch categories and author, or we
    #hardcode them, as they never change
    post = {}
    post['title'] = wp_post['title']['rendered']
    post['date'] = wp_post['date']
    post['author'] = wp_post['author']
    post['categories'] = wp_post['categories']
    post['content'] = wp_post['content']['rendered']
    if wp_post['content']['protected'] == 'true':
        post['visible'] = False
    else:
        post['visible'] = True
    post['image'] = wp_post['jetpack_featured_media_url']
    #assert False
    return render(request, 'wordpress/wp_detail.html', {'post': post,
    })
