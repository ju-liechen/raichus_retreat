from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import Post


def index(request):
    return render(request, 'index.html')


class BlogView(ListView):
    model = Post
    template_name = 'blog/posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.all()

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        if request.htmx:
            html = render_to_string(
                'blog/post_list.html', context, request)
            return HttpResponse(html)
        return self.render_to_response(context)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = {'post': self.object}
        html = render_to_string('blog/post_detail.html', context, request)
        return HttpResponse(html)
