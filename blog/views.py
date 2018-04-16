# from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from .models import Post, Tag, Category
import markdown

# Create your views here.


# def index(request):
#     return render(request,'blog/base.html',context={'title': '我的博客首页', 'welcome': '欢迎访问我的博客首页'})

def index(request):
    post_list = Post.objects.all().order_by('-create_time')
    tag_list = Tag.objects.all()
    category_list = Category.objects.all()
    return render(request, 'blog/index.html', context={'post_list': post_list,'tag_list': tag_list, 'category_list': category_list})

def detail(request,pk):
    post = get_object_or_404(Post, pk=pk)
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])
    return render(request,'blog/detail.html',context={'post': post})

def archives(request,year,month):
    post_list = Post.objects.filter(create_time__year=year,
                                    create_time__month=month
                                    ).order_by('-create_time')
    return render(request,'blog/index.html',context={'post_list': post_list})

def category(request,pk):
    cate = get_object_or_404(Category,pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-create_time')
    return render(request,'blog/index.html',context={'post_list': post_list})