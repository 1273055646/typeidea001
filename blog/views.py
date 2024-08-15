from datetime import date

from django.core.cache import cache
from django.views.generic import DetailView, ListView
from django.shortcuts import get_object_or_404
from django.db.models import Q, F

from config.models import SideBar
from .models import Post, Tag, Category
from comment.forms import CommentForm
from comment.models import Comment


class CommonViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'sidebars': SideBar.objects.all()
        })
        context.update(Category.get_navs())
        return context


class IndexView(CommonViewMixin, ListView):
    queryset = Post.latest_posts()
    paginate_by = 5
    context_object_name = 'post_list'
    template_name = 'blog/list.html'


class CategoryView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        context.update({
            'category': category,
        })
        return context

    def get_queryset(self):
        """ 重写 queryset，根据分类过滤 """
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)


class TagView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update({
            'tag': tag,
        })
        return context

    def get_queryset(self):
        """ 重写 queryset，根据标签过滤 """
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag_id=tag_id)


class PostDetailView(CommonViewMixin, DetailView):
    queryset = Post.latest_posts()
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get(self, request, *args, **kwargs):
        """ 重写了DetailView的get方法。在调用父类的get方法后（负责渲染页面），调用了自定义的handle_visited方法来处理访问量的增加。"""
        response = super().get(request, *args, **kwargs)
        self.handle_visited()
        return response

    def handle_visited(self):
        increase_pv = False  # 用于标记是否需要增加页面浏览量（PV）。
        increase_uv = False  # 用于标记是否需要增加独立访客数（UV）。

        uid = self.request.uid  # 从请求对象（self.request）中获取uid

        # pv_key 和 uv_key: 分别用于缓存PV和UV的键，它们由用户ID、日期（对于UV）和请求路径组成，以确保缓存的唯一性。
        pv_key = 'pv:%s:%s' % (uid, self.request.path)  # 构造uv_key，用于缓存当前用户在当前页面的UV访问情况。这里还包含了日期信息，以确保UV是按天计算的。
        uv_key = 'uv:%s:%s:%s' % (uid, str(date.today()), self.request.path)

        if not cache.get(pv_key):
            """
            使用cache.get(uv_key)检查缓存中是否已存在该键。
            如果不存在，说明用户尚未在今天内访问过该页面，
            因此将increase_uv设置为True，并设置缓存（有效期为24小时），表示用户已访问。
            """
            increase_pv = True
            cache.set(pv_key, 1, 1 * 60)  # 1分钟有效

        if not cache.get(uv_key):
            increase_uv = True
            cache.set(uv_key, 1, 24 * 60 * 60)  # 24小时有效

        if increase_pv and increase_uv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv') + 1, uv=F('uv') + 1)
        elif increase_pv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv') + 1)
        elif increase_uv:
            Post.objects.filter(pk=self.object.id).update(uv=F('uv') + 1)


class SearchView(IndexView):
    def get_context_data(self):
        context = super().get_context_data()
        context.update({
            'keyword': self.request.GET.get('keyword', '')
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get('keyword')
        if not keyword:
            return queryset
        return queryset.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword))


class AuthorView(IndexView):
    def get_queryset(self):
        queryset = super().get_queryset()
        author_id = self.kwargs.get('owner_id')
        return queryset.filter(owner_id=author_id)
