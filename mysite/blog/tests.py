from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.test import TestCase

# Create your tests here.
from .models import Post


class TestViews(TestCase):

    def setUp(self):
        self.author = User.objects.create()
        self.post = Post.objects.create(author=self.author,
                                        published_date=timezone.now() - timezone.timedelta(days=1),
                                        title="cane", text="bel")

    def test_post_list_return_200(self):
        """
        test that the post list view return 200
        """
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)

    def test_post_list_return_posts(self):
        """
        test that the post list contains our posts
        """
        response = self.client.get(reverse('post_list'))
        self.assertContains(response, '<h1><a href="/post/{}/">{}</a></h1>'
                            .format(self.post.pk, self.post.title))

    def test_post_published_date_greater_than_now_is_not_visualized(self):
        """
        it works
        """
        post = Post.objects.create(author=self.author,
                                   published_date=timezone.now() + timezone.timedelta(days=20))
        response = self.client.get(reverse('post_list'))
        self.assertNotContains(response, '<h1><a href="/post/{}/"></a></h1>'.format(post.pk))

    def test_post_detail_title_and_txt(self):
        """
        check the title and the text of the post
        """
        response = self.client.get(reverse('post_detail', args=(self.post.pk, )))
        self.assertContains(response, '<h1>{}</h1>'
                            .format(self.post.title))
        self.assertContains(response, '<p>{}</p>'.format(self.post.text))

    def test_post_detail_return_200(self):
        """
        check if post detail return 200
        """
        response = self.client.get(reverse('post_detail', args=(self.post.pk, )))
        self.assertEqual(response.status_code, 200)

    def test_post_detail_pk_invented(self):
        """
        if the posts doesn't exist return 404
        """
        response = self.client.get(reverse('post_detail', args=(21234, )))
        self.assertEqual(response.status_code, 404)

    def test_new_post_does_not_create(self):
        """
        check post is not created if data is invalid
        """
        response = self.client.post(reverse('post_new'), data={})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Post.objects.count(), 1)

    def test_new_post_works(self):
        """
        it works
        """
        data = {'title': 'puzza', 'text': 'lop'}
        User.objects.create_user('franco', password='123456', email='a@a.it')
        self.client.login(username='franco', password='123456')
        response = self.client.post(reverse('post_new'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('post_list'), response.url)
        post = Post.objects.filter(title='puzza')
        self.assertEqual(len(post), 1)

    def test_new_post_without_title(self):
        """
        it works
        """
        response = self.client.post(reverse('post_new'), data={'text': 'puzza'})
        self.assertEqual(response.status_code, 200)
        posts = Post.objects.filter(text='puzza')
        self.assertEqual(posts.count(), 0)

    def test_post_edit(self):
        """
        test edit fuction, it works
        """
        User.objects.create_user('franco', password='123456', email='a@a.it')
        self.client.login(username='franco', password='123456')
        response = self.client.post(reverse('post_edit',  args=(self.post.pk, )),
                                    data={'title': 'mubarack', 'text': 'lol'})
        self.assertEqual(response.status_code, 302)
        post = Post.objects.get(pk=self.post.pk)
        self.assertEqual(post.title, 'mubarack')
        self.assertEqual(post.text, 'lol')

    def test_post_delete_confirmation(self):
        """
        delete post, it works
        """
        response = self.client.get(reverse('post_delete', args=(self.post.pk, )))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)

    def test_post_does_not_exist_after_delete(self):
        response = self.client.post(reverse('post_delete', args=(self.post.pk, )))
        self.assertEqual(response.status_code, 302)
        post = Post.objects.filter(text='cane')
        self.assertEqual(post.count(), 0)
