from django.shortcuts import render,get_object_or_404,redirect
from blog.models import Post

from .models import Comment
from .forms import CommentForm

# Create your views here.


def post_comment(request,post_pk):
    """将评论与文章进行关联"""
    post = get_object_or_404(Post,pk=post_pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()

            return redirect(post)
        else:
            comment_list = post.comment_set.all()
            context = {'post': post,
                       'form': form,
                       'comment_list': comment_list
                       }
            return render(request,'blog/detail.html',context=context)

    # 不是post请求，说明该用户没有提交数据，重定向到文章详情页；
    return redirect(post)  # redirect方法如果接收一个模型的实例作为参数，那么这个参数必须实现了get_absolute_url方法，redirect会根据
                            # get_absolute_url方法返回的URL值进行重定向；


