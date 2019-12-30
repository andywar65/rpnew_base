import requests
from django.shortcuts import render

target = 'https://rifondazionepodistica.it/wp-json/wp/v2/'

def wp_list_view(request):
    filter = 'posts?_fields=title,link,excerpt&per_page=12'
    response = requests.get(target + filter )
    wp_posts = response.json()
    posts = []
    for wp_post in wp_posts:
        post = {}
        post['link'] = wp_post['link']
        post['title'] = wp_post['title']['rendered']
        post['excerpt'] = wp_post['excerpt']['rendered']
        posts.append(post)
    return render(request, 'wordpress/list.html', {'posts': posts,
    })
