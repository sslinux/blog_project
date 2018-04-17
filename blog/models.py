from django.db import models
from django.contrib.auth.models import User
from django.utils.six import python_2_unicode_compatible
from django.urls import reverse
from django.utils.html import strip_tags
import markdown

# Create your models here.

# python_2_unicode_compatible 装饰其用于兼容python2
@python_2_unicode_compatible
class Category(models.Model):
    """分类Category，需要继承自models.Model类"""
    name = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.name

# python2中若不愿使用装饰器，可以用__unicode__方法替代__str__方法；


@python_2_unicode_compatible
class Tag(models.Model):
    """标签Tag，需要继承自models.Model类"""
    name = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    excerpt = models.TextField(blank=True)   # 文章的摘要，可以为空；
    create_time = models.DateTimeField(auto_now_add=True,editable=False)
    modified_time = models.DateTimeField(auto_now=True,editable=False)
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag,blank=True)   # 可以没有标签，也可以有多个标签；
    author = models.ForeignKey(User)
    views = models.PositiveIntegerField(default=0)


    def __str__(self):
        return self.title

    # 自定义get_absulute_url 方法；
    # 记得从django.urls中导入reverse函数
    def get_absolute_url(self):
        return reverse('blog:detail',kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-create_time', 'title']

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def save(self,*args,**kwargs):
        if not self.excerpt:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            self.excerpt = strip_tags(md.convert(self.body))[:54]

        # 调用父类的save方法将数据保存到数据库中：
        super(Post,self).save(*args,**kwargs)




