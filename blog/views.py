# from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from .models import Post, Tag, Category
import markdown
from comments.forms import CommentForm
from django.views.generic import ListView,DetailView

# Create your views here.


# def index(request):
#     return render(request,'blog/base.html',context={'title': '我的博客首页', 'welcome': '欢迎访问我的博客首页'})

# def index(request):
#     post_list = Post.objects.all()
#     tag_list = Tag.objects.all()
#     category_list = Category.objects.all()
#     return render(request, 'blog/index.html', context={'post_list': post_list,'tag_list': tag_list, 'category_list': category_list})


class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    # 指定paginate_by 属性后开启分页功能，其值代表每一页包含多少篇文章；
    paginate_by = 2
    # 如果不是用类视图，分页功能可以参考django.cor.paginator的相关文档；


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

# class PostDetailView(DetailView):
#     model = Post
#     template_name = 'blog/detail.html'
#     context_object_name = 'post'
#
#     def get(self,request,*args, **kwargs):
#         """重写get方法的目的是因为每当文章被访问一次，就得将文章阅读量+1"""
#         response = super(PostDetailView,self).get(request, *args, **kwargs)
#         self.object.increase_views()
#         return response
#
#     def get_object(self, queryset=None):
#         # 重写get_object方法的目的是因为需要对post的body进行渲染；
#         post = super(PostDetailView,self).get_object(queryset=None)
#         post.body = markdown.markdown(post.body,extensions=[
#                                                                 'markdown.extensions.extra',
#                                                                 'markdown.extensions.codehilite',
#                                                                 'markdown.extensions.toc',
#                                                             ])
#         return post
#
#     def get_context_data(self, **kwargs):
#         """重写get_context_data的目的是因为除了将post传递给模板外,还要将评论表单、post下的评论列表传递给模板。"""
#         context = super(PostDetailView,self).get_context_data(**kwargs)
#         form = CommentForm()
#         comment_list = self.object.comment_set.all()
#         context.update({
#             'form': form,
#             'comment_list': comment_list
#         })
#
#         return context

# 记得在顶部导入 DetailView
class PostDetailView(DetailView):
    # 这些属性的含义和 ListView 是一样的
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        # 覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
        # get 方法返回的是一个 HttpResponse 实例
        # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
        # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
        response = super(PostDetailView, self).get(request, *args, **kwargs)

        # 将文章阅读量 +1
        # 注意 self.object 的值就是被访问的文章 post
        self.object.increase_views()

        # 视图必须返回一个 HttpResponse 对象
        return response

    def get_object(self, queryset=None):
        # 覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
        post = super(PostDetailView, self).get_object(queryset=None)
        post.body = markdown.markdown(post.body,
                                      extensions=[
                                          'markdown.extensions.extra',
                                          'markdown.extensions.codehilite',
                                          'markdown.extensions.toc',
                                      ])
        return post

    def get_context_data(self, **kwargs):
        # 覆写 get_context_data 的目的是因为除了将 post 传递给模板外（DetailView 已经帮我们完成），
        # 还要把评论表单、post 下的评论列表传递给模板。
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list
        })
        return context

def archives(request,year,month):
    post_list = Post.objects.filter(create_time__year=year,
                                    create_time__month=month
                                    )
    return render(request,'blog/index.html',context={'post_list': post_list})

# def category(request,pk):
#     cate = get_object_or_404(Category,pk=pk)
#     post_list = Post.objects.filter(category=cate)
#     return render(request,'blog/index.html',context={'post_list': post_list})

# class CategoryView(ListView):
#     model = Post
#     template_name = 'blog/index.html'
#     context_object_name = 'post_list'
#
#     def get_queryset(self):
#         cate = get_object_or_404(Category,pk=self.kwargs.get('pk'))
#         return super(CategoryView, self).get_queryset().filter(category=cate)


class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category,pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)
