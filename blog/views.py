# from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from .models import Post, Tag, Category
import markdown
from comments.forms import CommentForm

# Create your views here.


# def index(request):
#     return render(request,'blog/base.html',context={'title': '我的博客首页', 'welcome': '欢迎访问我的博客首页'})

def index(request):
    post_list = Post.objects.all()
    tag_list = Tag.objects.all()
    category_list = Category.objects.all()
    return render(request, 'blog/index.html', context={'post_list': post_list,'tag_list': tag_list, 'category_list': category_list})

def detail(request,pk):
    post = get_object_or_404(Post, pk=pk)
    # 阅读量+1；
    post.increase_views()
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])
    form = CommentForm()
    comment_list = post.comment_set.all()
    context = {'post': post,
               'form': form,
               'comment_list': comment_list
               }
    return render(request,'blog/detail.html',context={'post': post})

def archives(request,year,month):
    post_list = Post.objects.filter(create_time__year=year,
                                    create_time__month=month
                                    )
    return render(request,'blog/index.html',context={'post_list': post_list})

def category(request,pk):
    cate = get_object_or_404(Category,pk=pk)
    post_list = Post.objects.filter(category=cate)
    return render(request,'blog/index.html',context={'post_list': post_list})