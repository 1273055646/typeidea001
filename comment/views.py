from django.shortcuts import redirect
from django.views.generic import TemplateView

from .forms import CommentForm


class CommentView(TemplateView):
    http_method_names = ['post']
    template_name = 'comment/result.html'

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST)  # 创建一个CommentForm实例，并使用POST请求中的数据填充它。
        target = request.POST.get('target')  # 从POST请求中获取target参数的值，这个值可能是一个URL，表示评论提交后要重定向到的页面。

        if comment_form.is_valid():  # 检查表单数据是否有效。
            instance = comment_form.save(commit=False)  # 如果表单有效，保存表单数据到一个模型实例中，但不立即提交到数据库。
            instance.target = target   # 设置模型实例的target属性。
            instance.save()  # 将模型实例保存到数据库。
            succeed = True  # 设置succeed变量为True，表示评论提交成功。
            return redirect(target)  # 重定向到target指定的URL。
        else:
            succeed = False   # 如果表单无效，设置succeed变量为False。

        context = {
            'succeed': succeed,
            'form': comment_form,
            'target': target,
        }
        return self.render_to_response(context)   # 使用context中的数据渲染模板，并返回渲染后的页面。