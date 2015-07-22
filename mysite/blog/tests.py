from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
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
        response = self.client.get(reverse('post_detail', args=(self.post.pk,)))
        self.assertContains(response, '<h1>{}</h1>'
                            .format(self.post.title))
        self.assertContains(response, '<p>{}</p>'.format(self.post.text))

    def test_post_detail_return_200(self):
        """
        check if post detail return 200
        """
        response = self.client.get(reverse('post_detail', args=(self.post.pk,)))
        self.assertEqual(response.status_code, 200)

    def test_post_detail_pk_invented(self):
        """
        if the posts doesn't exist return 404
        """
        response = self.client.get(reverse('post_detail', args=(21234,)))
        self.assertEqual(response.status_code, 404)

    def test_new_post_without_title(self):
        """
        it works
        """
        response = self.client.post(reverse('post_new'), data={'text': 'puzza'})
        self.assertEqual(response.status_code, 302)
        posts = Post.objects.filter(text='puzza')
        self.assertEqual(posts.count(), 0)

    def test_post_edit_without_login(self):
        """
        test edit fuction, it works
        """
        response = self.client.post(reverse('post_edit', args=(self.post.pk, )))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url='/accounts/login/?next=/post/1/edit/')

    def test_post_delete_confirmation_without_login(self):
        """
        delete post, it works
        """
        response = self.client.get(reverse('post_delete', args=(self.post.pk,)))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url='/accounts/login/?next=/post/1/delete/')

    def test_profile_user(self):
        User.objects.create_user('franco', password='123456', email='a@a.it')
        self.client.login(username='franco', password='123456')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'franco')

    def test_sign_in(self):
        response = self.client.get(reverse('register'))
        self.assertEquals(response.status_code, 200)

    def test_login(self):
        User.objects.create_user('franco', password='123456', email='a@a.it')
        self.client.login(username='franco', password='123456')
        response = self.client.get(reverse('login'))
        self.assertEquals(response.status_code, 200)

    def test_logout(self):
        User.objects.create_user('franco', password='123456', email='a@a.it')
        self.client.login(username='franco', password='123456')
        self.client.logout()
        response = self.client.get(reverse('logout'))
        self.assertEquals(response.status_code, 200)

    def test_edit_login_without_perm(self):
        User.objects.create_user('franco', password='123456', email='a@a.it')
        self.client.login(username='franco', password='123456')
        response = self.client.post(reverse('post_edit', args=(self.post.pk,)),
                                    data={'title': 'mubarack', 'text': 'lol'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url='/accounts/login/?next=/post/1/edit/')

    def test_delete_without_perm(self):
        User.objects.create_user('franco', password='123456', email='a@a.it')
        self.client.login(username='franco', password='123456')
        response = self.client.post(reverse('post_delete', args=(self.post.pk, )))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url='/accounts/login/?next=/post/1/delete/',)

    def test_new_post_without_perm(self):
        User.objects.create_user('franco', password='123456', email='a@a.it')
        self.client.login(username='franco', password='123456')
        response = self.client.post(reverse('post_new'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url='accounts/login/?next=/post/new/')

    def test_new_post_with_perms(self):
        user = User.objects.create_user('franco', password='123456', email='a@a.it')
        contentype = ContentType.objects.get_for_model(Post)
        can_add_post = Permission.objects.create(name='Can add post', codename='add_post',
                                                 content_type=contentype)
        user.user_permissions.add(can_add_post)
        self.assertTrue(user.has_perm('blog.add_post'))
        self.client.login(username='franco', password='123456')
        data = {'title': 'p', 'text': 'blbl'}
        response = self.client.post(reverse('post_new'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('post_list'), response.url)
        post = Post.objects.filter(title='p')
        self.assertEqual(len(post), 1)
