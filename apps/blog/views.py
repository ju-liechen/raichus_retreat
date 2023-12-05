from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import DetailView, ListView, CreateView

from .models import Category, Post


def index(request):
    return render(request, 'index.html')


class BlogView(ListView):
    model = Post
    template_name = 'blog/posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.all()

    def get(self, request):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        if request.htmx:
            html = render_to_string(
                'blog/posts.html', context, request)
            return HttpResponse(html)
        return self.render_to_response(context)

    def post(self, request):
        title = request.POST.get('title')
        body = request.POST.get('body')
        category = request.POST.get('category')

        category, _ = Category.objects.get_or_create(name=category)

        new_post = Post.objects.create(
            title=title,
            body=body,
            created_by=request.user,
            category=category)
        new_post.save()

        context = {'posts': Post.objects.all()}
        html = render_to_string('blog/post_list.html', context, request)
        return HttpResponse(html)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = {'post': self.object}
        html = render_to_string('blog/post_detail.html', context, request)
        return HttpResponse(html)
