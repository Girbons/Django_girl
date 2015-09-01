from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.decorators import method_decorator
from .models import Post, Comment
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View, \
    TemplateView
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from .form import RegistrationForm



class PostListView(ListView):
    model = Post
    queryset = Post.objects.all()

    def get_queryset(self):
        queryset = super(PostListView, self).get_queryset()
        return queryset.filter(published_date__lte=timezone.now()).order_by('-published_date')


class PostDetailView(DetailView):
    model = Post
    queryset = Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context.update({'comments': self.object.comment_set.all()})
        return context


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

    @method_decorator(permission_required('blog.add_post'))
    def dispatch(self, *args, **kwargs):
        return super(PostNew, self).dispatch(*args, **kwargs)


class PostEdit(UpdateView):
    model = Post
    fields = ('title', 'text')
    template_name = 'blog/post_edit.html'

    def get_success_url(self):
        return reverse('post_detail', args=(self.get_object().pk, ))

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostEdit, self).form_valid(form)

    @method_decorator(permission_required('blog.change_post'))
    def dispatch(self, *args, **kwargs):
        return super(PostEdit, self).dispatch(*args, **kwargs)

class PostDelete(DeleteView):
    model = Post

    def get_success_url(self):
        return reverse('post_list')

    @method_decorator(permission_required('blog.delete_post'))
    def dispatch(self, *args, **kwargs):
        return super(PostDelete, self).dispatch(*args, **kwargs)

class Registration(CreateView):
    model = get_user_model()
    template_name = 'accounts/register.html'
    form_class = RegistrationForm
    success_url = 'registration_complete'


class RegistrationComplete(TemplateView):
    template_name = 'accounts/registration_complete.html'


class Profile(ListView):
    model = get_user_model()
    template_name = 'accounts/profile.html'

class NewComment(CreateView):
    model = Comment
    fields = ('text', )
    template_name = 'blog/comment_edit.html'

    def get_success_url(self):
        return reverse('post_detail', args=(self.get_object().pk, ))

    def form_valid(self, form):
        form.instance.post = Post.objects.get(pk=self.kwargs.get('pk'))
        return super(NewComment, self).form_valid(form)


class CommentList(ListView):
    model = Comment
    queryset = Comment.objects.all()


class CommentEdit(UpdateView):
    model = Comment
    fields = ('text', 'post', )
    template_name = 'blog/comment_edit.html'

    def get_success_url(self):
        return reverse('post_detail', args=(self.get_object().pk, ))

    def form_valid(self, form):
        form.instance.post = Post.objects.get(pk=self.kwargs.get('pk'))
        return super(CommentEdit, self).form_valid(form)



class DeleteComment(DeleteView):
    model = Comment

    def get_success_url(self):
        return reverse('post_detail', args=(self.get_object().pk, ))
