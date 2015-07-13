from django.utils import timezone
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse


class PostListView(ListView):
    model = Post
    queryset = Post.objects.all()

    def get_queryset(self):
        queryset = super(PostListView, self).get_queryset()
        return queryset.filter(published_date__lte=timezone.now()).order_by('-published_date')


class PostDetailView(DetailView):
    model = Post
    queryset = Post.objects.all()


class PostNew(CreateView):
    model = Post
    fields = ('title', 'text', 'published_date')
    template_name = 'blog/post_edit.html'

    def get_success_url(self):
        return reverse('post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.published_date = timezone.now()
        return super(PostNew, self).form_valid(form)


class PostEdit(UpdateView):
    model = Post
    fields = ('title', 'text')
    template_name = 'blog/post_edit.html'

    def get_success_url(self):
        return reverse('post_detail', args=(self.get_object().pk, ))

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostEdit, self).form_valid(form)

class PostDelete(DeleteView):
    model = Post

    def get_success_url(self):
        return reverse('post_list')

