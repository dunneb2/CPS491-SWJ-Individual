from collections import Counter
from django import template
from ..models import Post
from django.db.models import Count
# from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(
        total_comments = Count('comments')
    ).order_by('-total_comments')[:count]


@register.simple_tag
def get_top_users(count=3):
    all_posts = Post.published.all()
    all_posts_authors = []
    for post in all_posts:
        all_posts_authors.append(post.author)
    
    # Creates a dictionary of keys and values where the keys are the authors
    # and the values are the number of occurances in all_post_authors
    author_count = Counter(all_posts_authors)

    # Create an list of the keys and sort it from the highest value to the lowest
    ordered_authors_list = list(author_count.keys())
    ordered_authors_list.sort(key=lambda x: author_count[x], reverse=True)
    
    # create a final list that is displayed that lookes like: "author (#)"
    final_display_list = []
    for author in ordered_authors_list:
        final_display_list.append(str(author) + " (" + str(author_count[author]) + ")")

    return final_display_list[:count]

    
    